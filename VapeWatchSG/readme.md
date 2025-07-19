# 🚭 VapeWatch SG – AI-Powered Anti-Vape Surveillance System
## Author: Rohit Panda
## 📌 Overview

VapeWatch SG is a personal project inspired by the Straits Times article on the Health Sciences Authority's initiative to acquire a cyber surveillance tool targeting illegal vape activity in Singapore.

This project simulates a lightweight AI-enabled platform that monitors and analyzes online content (e.g., Telegram, forums, marketplaces) for illicit e-vaporiser sales, with a focus on Kpod-related risks.

## 🎯 Objectives

- Detect illegal vape-related content across online platforms
- Analyze posts and score user profiles by risk level
- Provide a web-based dashboard for real-time monitoring
- Raise awareness of public health threats like Kpods

## 🧠 Features

- 🔍 **Keyword & Slang Detection** (e.g., "Kpod", "grape juice" = vape juice)
- 🧠 **AI-Based Risk Scoring** (based on content frequency, language, user metadata)
- 🌐 **Telegram Scraper** using Telethon or Telegram API
- 📊 **Dashboard** for visualization of alerts, risk scores, user profiles
- 🌍 **(Optional) Location-based insights** using geotagged metadata

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python, JavaScript |
| NLP/AI | spaCy / Scikit-learn / OpenAI API (optional) |
| Web Scraping | BeautifulSoup, Telethon |
| Backend/API | Flask / FastAPI |
| Frontend | React / Streamlit (MVP) |
| Database | MongoDB / SQLite |
| Visualization | Chart.js / D3.js / Plotly |

## 📁 Project Structure

```bash

```

## 📈 Risk Scoring Method (Example)

| Factor | Weight |
|--------|--------|
| Vape-related keyword match | 40% |
| Frequency of posts | 25% |
| Metadata patterns (e.g., phone reused) | 20% |
| Obfuscated or slang terms | 15% |

## ⚠️ Disclaimer

This project is for educational and research purposes only. It simulates features relevant to cybersecurity and public health surveillance without accessing private data or real-world users. It does not promote, facilitate, or condone illegal monitoring.

## 📚 Inspiration

- HSA Anti-Vape Surveillance Tool News
- Singapore Poisons Act & Tobacco Regulation laws
- Public health campaigns against vaping in Singapore