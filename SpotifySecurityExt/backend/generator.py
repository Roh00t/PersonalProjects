import asyncio
import logging
import os
import spacy
import requests
import spotipy
import numpy as np
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from spotipy.oauth2 import SpotifyOAuth
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from functools import lru_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

spacy.prefer_gpu()  

load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

class PlaylistGenerator:
    def __init__(self):
        self.emotion_classifier = pipeline("text-classification", model="joeddav/distilbert-base-uncased-go-emotions-student", top_k=1)
        self.embedder = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    def classify_mood(self, user_prompt):
        """
        Uses a pretrained NLP model to classify mood dynamically
        """
        emotions = self.emotion_classifier(user_prompt)
        if emotions:
            return emotions[0][0]["label"]  # Extract highest confidence emotion label
        return "neutral"

    def get_user_top_songs(self, sp):
        """
        Fetches the user's top 50 tracks from Spotify
        """
        results = sp.current_user_top_tracks(limit=50, time_range="medium_term")
        tracks = []

        for item in results["items"]:
            track_id = item["id"]
            track_name = item["name"]
            artist = item["artists"][0]["name"]
            tracks.append({"id": track_id, "name": track_name, "artist": artist})

        return tracks

    @lru_cache(maxsize=500)
    def get_song_info(self, song_name, artist_name):
        """
        Fetches metadata (tags, moods, etc.) for a given song from Last.fm.
        Implements caching to optimize performance.
        """
        try:
            url = "http://ws.audioscrobbler.com/2.0/"
            params = {
                "method": "track.getInfo",
                "api_key": LASTFM_API_KEY,
                "artist": artist_name,
                "track": song_name,
                "format": "json"
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "track" in data:
                tags = [tag["name"] for tag in data["track"]["toptags"]["tag"]]
                return {"song": song_name, "artist": artist_name, "tags": tags}
            return None
        except requests.RequestException as e:
            logger.error(f"Error fetching song info: {e}")
            return None

    async def get_songs_from_playlist(self, sp, playlist_id):
        """
        Fetches the top global playlist from Spotify asynchronously.
        """
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, sp.playlist_tracks, playlist_id)

        return [
            {
                "id": track["track"]["id"],
                "name": track["track"]["name"],
                "artist": track["track"]["artists"][0]["name"],
                "image": sp.track(track["track"]["id"])["album"]["images"][0]["url"]
            }
            for track in results["items"]
        ]

    def get_embedding(self, prompt):
        """
        Embeds piece of text into latent space
        """
        return self.embedder.encode(prompt)

    def create_playlist(self, sp, mood, recommended_tracks):
        """
        Creates a Spotify playlist and adds the recommended tracks
        """
        playlist = sp.user_playlist_create(user=sp.current_user()["id"], name=mood, public=True)
        track_uris = [f"spotify:track:{track}" for track in recommended_tracks]
        sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)
        return playlist["external_urls"]["spotify"]

    def generate_playlist(self, sp, token, user_prompt, username):
        """
        Generates a Spotify playlist based on user mood dynamically with optimized processing.
        """
        try:
            # Classify mood using NLP
            mood = self.classify_mood(user_prompt)
            if not mood:
                raise ValueError("NLP model unable to classify mood.")
            embedded_mood = self.get_embedding(mood)
            
            logger.info(f"Detected Mood: {mood}")

            # Fetch user top tracks in parallel
            with ThreadPoolExecutor() as executor:
                future_user_tracks = executor.submit(self.get_user_top_songs, sp)
                future_global_tracks = executor.submit(self.get_songs_from_playlist, sp, "1RDk6T6DZNnYvBaBZQ3eWh")

                user_top_tracks = future_user_tracks.result()
                global_top_tracks = future_global_tracks.result()

            if not user_top_tracks:
                raise ValueError("No top tracks found for user.")

            # Embed tracks for similarity search
            embedded_user_tracks = {
                track["id"]: self.get_embedding(' '.join(self.get_song_info(track['name'], track['artist'])['tags']))
                for track in user_top_tracks
            }

            embedded_global_tracks = {
                track["id"]: self.get_embedding(' '.join(self.get_song_info(track['name'], track['artist'])['tags']))
                for track in global_top_tracks
            }

            # Compute user profile embedding
            user_top_embeddings = np.array([
                embedded_global_tracks[track] for track in embedded_user_tracks if track in embedded_global_tracks
            ])
            user_profile_embedding = np.mean(user_top_embeddings, axis=0) if user_top_embeddings.size != 0 else np.zeros(
                (list(embedded_global_tracks.values())[0].shape[0],)
            )

            # Perform similarity search
            knn = NearestNeighbors(n_neighbors=50, metric="cosine")
            knn.fit(np.array(list(embedded_global_tracks.values())))
            distances, indices = knn.kneighbors([embedded_mood])
            indices = [int(idx) for _, idx in sorted(zip(distances[0], indices[0]))]
            closest_global_songs = {
                list(embedded_global_tracks.items())[idx][0]: list(embedded_global_tracks.items())[idx][1] for idx in indices
            }

            # Rank recommended songs
            similarities = cosine_similarity(np.array(list(closest_global_songs.values())),
                                             user_profile_embedding.reshape(1, -1))
            sorted_indices = np.argsort(similarities[:, 0])[::-1]
            recommended_songs = [list(closest_global_songs.keys())[i] for i in sorted_indices[:25]]

            if not recommended_songs:
                raise ValueError("No suitable songs found for this mood.")

            # Create and return the playlist
            playlist_url = self.create_playlist(sp, user_prompt, recommended_songs)
            new_playlist_tracks = self.get_songs_from_playlist(sp, playlist_url.split('/')[-1])
            playlist_name = 'Generated Playlist'

            return {
                "success": True,
                "playlist_url": playlist_url,
                "playlist_name": playlist_name,
                "playlist_tracks": new_playlist_tracks
            }
        except Exception as e:
            logger.error(f"Error generating playlist: {e}")
            return {"success": False, "message": str(e)}