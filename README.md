# 🎵 Spotify ML Analyzer: Your Musical DNA Decoded

![Status](https://img.shields.io/badge/Status-In%20Development-yellow) ![Stack](https://img.shields.io/badge/Stack-Full%20Stack%20Data%20Science-blueviolet)

> **Note:** This project is currently under active development. I am documenting the entire process publicly.

## 💡 The Idea

Most apps tell you *what* you listen to (artists or songs). **Spotify ML Analyzer** explains **who you are** through your music.

This application acts as a "Psychological Musical Mirror." It uses Data Science algorithms to extract complex audio metrics from the Spotify API—such as "Valence" (positivity), "Energy," and "Danceability"—and processes them into an interactive dashboard that reveals your current mood and how your taste evolves over time.

### Project Goals (MVP)
* **Real Authentication:** Secure login via Spotify (OAuth 2.0).
* **Deep Analysis:** Extraction of "Audio Features" hidden from the official app.
* **Persistence:** Save "snapshots" of your taste to compare "Today vs. Last Month."
* **Visualization:** Radar Charts (Spider Charts) to understand your profile at a glance.

---

## Tech Stack

This project implements a decoupled architecture to simulate a real-world "Full Stack Data Science" production environment:

### Backend (Logic & Data)
* **Python & Django REST Framework:** Robust and secure API.
* **Pandas & NumPy:** Statistical processing and music data cleaning.
* **SQLite3:** Data persistence (Local Development).

### Frontend (User Experience)
* **React.js (Vite):** Dynamic and fast UI.
* **Recharts:** Data visualization library for radar charts.
* **Bootstrap 5:** Responsive and clean layout.

---

## Development Roadmap

I am using an "Atomic Development" methodology to build this step-by-step:

- [ ] **Phase 1: Foundations** (Monorepo Setup, Django & React configurations).
- [ ] **Phase 2: The Handshake** (OAuth 2.0 Authentication with Spotify).
- [ ] **Phase 3: Data Pipeline** (Data extraction and processing with Pandas).
- [ ] **Phase 4: Visualization** (Interactive Frontend and Charts).

---

## 📝 Development Log (DevLog)

I strongly believe in "building in public." You can follow the technical challenges, architecture decisions, and bugs I while building this project:

[Read the DEVLOG.md](./DEVLOG.md)

---
*Developed by Aníbal Rojo*