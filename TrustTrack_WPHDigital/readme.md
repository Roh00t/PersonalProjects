# TrustTrack 🛡️🎙️
## Author: Rohit Panda
**Ethical Voice-Driven Time Logging for Professionals**

TrustTrack is a privacy-first, AI-powered time tracking tool designed for mobile-first professionals and field workers. It enables users to log time using natural voice commands without compromising privacy or morale.

---

## 🚀 Features

- 🎙️ **Voice-powered time entry**: "Log 45 minutes for content planning"
- 🤖 **AI/NLP parsing** with Whisper + OpenAI
- 📱 **Offline-first mobile/web app** (Flutter or React Native)
- 🔒 **End-to-end encrypted logs**
- 📊 **Intuitive summaries and insights**
- 🧠 **Categorization without surveillance** (no screenshots or keystroke tracking)

---

## 🌟 Why TrustTrack?

Most time trackers today rely on invasive monitoring. TrustTrack offers a refreshing alternative: accurate, effortless time logging with **full user control and zero surveillance**. Built for people who value time *and* trust.

---

## 📸 Demo

> 🎥 Screenshots, GIFs, or Figma Prototype link here

- [🖼️ View Figma Prototype (Coming Soon)](#)
- [📽️ Live demo video (Coming Soon)](#)

---

## ⚙️ Tech Stack

| Layer            | Tools Used                          |
|------------------|-------------------------------------|
| Frontend         | Flutter / React Native              |
| Backend          | Node.js + Express / Firebase        |
| NLP & Voice      | Whisper (Speech) + OpenAI API       |
| Database         | SQLite (offline), Supabase (cloud)  |
| Auth & Sync      | Supabase Auth / Firebase Auth       |
| Security         | AES local encryption                |

---

## 🧪 How to Run Locally

1. **Clone the repo**

2. **Install dependencies**
   ```bash
   npm install # or flutter pub get
   ```

3. **Set environment variables**
   
   Create a `.env` file and add:
   ```ini
   OPENAI_API_KEY=your-key
   SUPABASE_URL=your-url
   SUPABASE_ANON_KEY=your-key
   ```

4. **Run the app**
   ```bash
   npm run dev # or flutter run
   ```

---

## 📁 Project Structure

```bash
/client     → Mobile/frontend app (Flutter or React Native)
/server     → API logic, NLP, auth
/models     → Task, Log, User schemas
/docs       → Business plan, research paper, Figma links
```

---

## 🔐 Privacy Philosophy

TrustTrack is built with:

- **Zero surveillance principles**
- **Local-first logging** with user-owned data
- **Transparent, minimal data collection**