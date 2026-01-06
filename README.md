# 🎵 Spotify ML Analyzer: Your Musical DNA Decoded

![Status](https://img.shields.io/badge/Status-In%20Development-yellow) ![Stack](https://img.shields.io/badge/Stack-Full%20Stack%20Data%20Science-blueviolet)

> **Note:** This project is currently under active development. I am documenting the entire process publicly.

## The Idea

Most apps tell you *what* you listen to (artists or songs). **Spotify ML Analyzer** explains **who you are** through your music.

This application acts as a "Psychological Musical Mirror." It connects to your Spotify account, extracts complex audio metrics—such as "Valence" (positivity), "Energy," and "Danceability"—and uses Unsupervised Machine Learning to group your taste into personality profiles. Finally, an AI Agent interprets these profiles to give you a text-based psychological analysis.

### Project Goals (MVP)
* **Real Authentication:** Secure login via Spotify (OAuth 2.0).
* **Deep Analysis:** Extraction of "Audio Features" hidden from the official app.
* **ML Profiling:** Using **K-Means Clustering** to identify your distinct musical moods.
* **AI Insights:** Integration with **OpenAI** to generate personality descriptions.
* **Visualization:** Radar Charts & Scatter Plots to see your cluster distribution.

---

## Project Documentation

Beyond the code, this project follows rigorous engineering practices. You can read the detailed specifications here:

| Document | Description |
| :--- | :--- |
| **[Product Requirements (PRD)](./docs/PDR.md)** | Features, User Stories, and MVP scope definition. |
| **[Architecture Design (TDD)](./docs/ARCHITECTURE.md)** | System design, "Store-First" strategy, and Database Schema. |

---

## Technical Architecture

This project uses a **Decoupled Client-Server Architecture** with a **Synchronous Monolithic Backend**. It implements a "**Store-First, Analyze-Later**" strategy to handle heavy ML processing without blocking the user experience.

![App Architecture](docs/images/app_architecture.png)

--- 


## Tech Stack

This project implements a decoupled architecture to simulate a real-world "Full Stack Data Science" production environment:

### Backend (Logic & Data)
* **Python/Django REST Framework:** Main API and Business Logic.
* **Pandas/NumPy:** Statistical processing and music data cleaning.
* **Scikit-learn:** K-Means Clustering and Data Normalization (StandardScaler)
* **PostgreSQL**: Production-grade database (Deployed on Railway).

### Frontend (User Experience)
* **React.js (Vite):** Dynamic UI with asynchronous state management.
* **Recharts:** Data visualization library for radar charts.

---

## Development Roadmap

This project follows a phased evolutionary path, simulating a real-world "Full Stack Data Science" product cycle.

> ⚠️ **Project Status Update (Jan 2025):** Due to temporary restrictions on the Spotify Developer Dashboard, this project has pivoted to a **"Simulation Architecture"**. Instead of live API calls, the backend currently utilizes a rich **Kaggle Dataset (30k+ songs)** and a **Mock Authentication Layer** to emulate the full application flow. The logic remains production-ready for when API access is restored.

### **Phase 1: Infrastructure & Data Analysis** (✅ Completed)
**Goal:** Project setup and understanding the data.
* Monorepo & Django configuration.
* **EDA (Exploratory Data Analysis):** Analyzed the Kaggle dataset to understand feature distributions (Valence vs Energy).
* **Prototype:** Trained the initial K-Means model using the static dataset (`k=5` clusters).

### **Phase 2: The "Offline" Backend & AI** (In Progress)
**Goal:** Building the core API services using Simulation Data.
* **ETL:** Ingesting the Kaggle CSV into PostgreSQL to simulate the User's library.
* **Mock Auth:** Bypassing Spotify's OAuth for local development.
* **GenAI Agent:** Integrating **Gemini** to generate textual, psychological insights based on the "Offline" clusters.
* **API:** Exposing the ML results via Django REST Framework endpoints.

### **Phase 3: Frontend Visualization** (Pending)
**Goal:** Building the reactive User Interface.
* Connecting React to the Django "Mock" API.
* Translating raw JSON data into interactive Radar Charts and Scatter Plots.
* Displaying the LLM-generated personality insights.

### **Phase 4: Production & Deployment** (Pending)
**Goal:** Getting the MVP live.
* Final optimization and Dockerization.
* Cloud deployment (Railway/Vercel) allowing public access to the "Simulated" demo.

### **Phase 5: The "Live" Switch** (Future)
**Goal:** Transitioning from Simulation to Real Data (Once API access is granted).
* Activating real OAuth 2.0.
* Swapping the CSV Ingestor for the live Spotify `spotipy` client.
* Validating ML model performance with real-time user data.

---

## 📝 Development Log (DevLog)

I strongly believe in "building in public". You can follow the technical challenges, architecture decisions, and bugs I encounter while building this project:

[Read the DEVLOG.md](./DEVLOG.md)

---
*Developed by Aníbal Rojo*