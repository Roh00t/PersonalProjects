import speech_recognition as sr
from twilio.rest import Client

# Define emergency keywords
EMERGENCY_KEYWORDS = ["help", "fire", "stop", "emergency"]

# Twilio setup (replace with your credentials)
ACCOUNT_SID = ""
AUTH_TOKEN = ""
FROM_PHONE = ""
TO_PHONE = ""

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_alert(keyword):
    """Send an alert via SMS when an emergency is detected."""
    message = client.messages.create(
        body=f"Emergency detected: '{keyword}' was shouted!",
        from_=FROM_PHONE,
        to=TO_PHONE
    )
    print(f"Alert sent: {message.sid}")

def listen_for_keywords():
    """Capture audio and detect emergency keywords."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for emergency phrases...")
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio).lower()
            print(f"Detected speech: {text}")
            
            # Check for emergency keywords
            for keyword in EMERGENCY_KEYWORDS:
                if keyword in text:
                    print(f"Emergency keyword detected: {keyword}")
                    send_alert(keyword)
                    break
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")

if __name__ == "__main__":
    listen_for_keywords()
