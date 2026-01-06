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

---

## Development Roadmap

This project follows a 5-stage evolutionary path, moving from local simulation to a production-ready Full Stack application.

> ⚠️ **Project Status Update (Jan 2025): Due to temporary restrictions on the Spotify Developer Dashboard (blocking new app creation), this project has pivoted to a **"Simulation Architecture"**. Instead of live API calls, the backend now uses a rich **Kaggle Dataset (30k+ songs)** and a **Mock Authentication Layer** to emulate the full application flow. The logic remains production-ready for when API access is restored.

### **Phase 1: Infrastructure & Foundations** (✅ Completed)
> **Goal:** Monorepo setup, environment configuration, and technology stack initialization (Django + React).

### **Phase 2: Data Engineering & ML Core** (In Progress)
> **Goal:** Implementing the "Simulation Engine." This involves processing the raw Kaggle dataset (30k+ songs), performing EDA, and integrating the K-Nearest Neighbors (KNN) algorithm directly into the backend logic.

### **Phase 3: API Services & AI Integration** (Pending)
> **Goal:** Exposing the data through a robust Django REST API.
> * **Mock Auth:** Bypassing Spotify's OAuth for development.
> * **GenAI Agent:** Integrating an **LLM (Large Language Model)** to generate textual, psychological insights based on the user's musical DNA.

### **Phase 4: Frontend Visualization & Dashboard** (Pending)
> **Goal:** Building the reactive User Interface. Translating raw JSON data into interactive Radar Charts, Scatter Plots, and displaying the LLM-generated insights.

### **Phase 5: Production Polish & Deployment** (Pending)
> **Goal:** Final optimization, Dockerization, and cloud deployment (Railway/Vercel). Preparation for the potential switch from "Mock Data" to live Spotify API integration.

---

## 📝 Development Log (DevLog)

I strongly believe in "building in public." You can follow the technical challenges, architecture decisions, and bugs I while building this project:

[Read the DEVLOG.md](./DEVLOG.md)

---
*Developed by Aníbal Rojo*