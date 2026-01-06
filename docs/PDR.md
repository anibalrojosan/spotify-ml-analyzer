# Product Requirements Document: Spotify ML Analyzer

| Metadata | Details |
| :--- | :--- |
| **Project Name** | Spotify ML Analyzer |
| **Version** | 2.0 (Simulation Pivot) |
| **Status** | Phase 2: In Development |
| **Owner** | Aníbal Rojo |
| **Last Updated** | Jan 2026 |

---

## 1. Context & Problem Statement
### 1.1 The Problem (The "Why")
Spotify excels at recommending music, but its algorithms operate as a "black box." Power users lack access to deep metrics (Audio Features) and do not understand *why* specific content is suggested. Furthermore, current restrictions on the Spotify Developer Dashboard have blocked the creation of new apps, hindering standard API integration development.

### 1.2 The Solution (Opportunity)
A resilient **"Full Stack Data Science"** application. Instead of relying solely on live API calls, the system implements a **"Simulation Mode"** using a massive Kaggle dataset. It offers a **Psychological Dashboard** that translates technical data (valence, energy) into human emotions and integrates a **GenAI Agent (LLM)** that acts as a personalized "Music Psychologist."

---

## 2. Product Goals
1.  **Technical Resilience:** Demonstrate a decoupled architecture capable of operating in "Offline/Simulation Mode" (Local Dataset) while remaining ready for "Online Mode" (Real API).
2.  **Advanced Profiling:** Visualize the user's "Musical DNA" using Scatter Plots and Radar Charts, moving beyond simple text lists.
3.  **GenAI Personality:** Leverage Large Language Models (LLMs) to generate unique, humorous, or analytical narratives ("Roasts" or Psychoanalysis) based on user data.

---

## 3. User Personas
* **The Quantified Self:** Loves data. Wants to know: *"Is my music 20% sadder during winter?"* or *"How does my energy preference evolve over years?"*
* **The Sonic Explorer:** Feels trapped in the mainstream algorithm. Wants tailored recommendations based on mathematical parameters (e.g., "Give me a track with `Energy > 0.8` but `Popularity < 30`").

---

## 4. Data Strategy (Simulation Layer)
*Due to the API blockage, the project currently operates in "Simulation Mode".*

* **Source of Truth:** Static Kaggle Dataset (`cleaned_dataset.csv`) hosted in `backend/data/`.
* **Volume:** ~30,000 tracks containing full metadata and Audio Features.
* **User Simulation:**
    * The system acts as a "Mock Server."
    * It generates a "Fake Profile" by randomly selecting a subset of songs from the dataset to simulate a `Recently Played` history.
    * This allows for full testing of ML algorithms without requiring real user data.

### 4.1 Simulated User Archetypes (Cluster Definitions)
To validate the application's ability to handle diverse musical tastes, the system initializes with **5 Pre-calculated Archetypes**. These were derived using K-Means Clustering on the dataset (`3.0-model-clustering-profiles`), segmenting users based on distinct Audio Feature patterns.

These profiles act as the "selectable characters" during the Mock Login phase:

| Cluster ID | Profile Name | Archetype Definition (Business Logic) | Key Trigger Features |
| :--- | :--- | :--- | :--- |
| **Cluster 3** | **The Organic / Relaxed** | User seeks calmness, disconnection, or focus. Prefers natural sounds over synthesized production. Likely engages in "Deep Work" or relaxation. | `High Acousticness`, `Low Energy` |
| **Cluster 4** | **The Euphoric / Social** | User seeks dopamine and social connection. Prefers music that is explicitly happy and danceable. Indicative of "Party" or "Mood-Lifting" sessions. | `Max Valence`, `Max Danceability` |
| **Cluster 1** | **The High Intensity** | User seeks adrenaline and power. Prefers fast, aggressive, or heavy music (Metal, Hard Techno, Gym). Focus is on physical stimulation, not necessarily happiness. | `Max Tempo (>130 BPM)`, `Max Energy` |
| **Cluster 0** | **The Rhythmic Flow** | User seeks momentum and consistency. Prefers the steady 120-128 BPM range (House, Modern Pop) that maintains a "Flow State" without emotional extremes. | `Fixed Tempo (~125 BPM)`, `High Energy` |
| **Cluster 2** | **The Mainstream Groove** | User seeks accessibility and balance. Prefers polished, radio-friendly structures with a good groove. Represents the versatile "middle ground" listener. | `High Danceability`, `Mid-High Energy` |

---

## 5. Functional Requirements

### 5.1 Authentication (Mock Auth Layer)
* **Feature:** `MockLoginView`.
* **Description:** A login system that bypasses OAuth 2.0. Upon clicking "Login," the backend generates a temporary JWT token and assigns a dummy user profile (Avatar, Name, Simulated History).
* **Goal:** Enable Frontend and Session development without depending on valid Spotify Client IDs.

### 5.2 Analytics Dashboard (Visualization Core)
* **Psychological Map (Scatter Plot):**
    * *X-Axis:* Valence (Positivity).
    * *Y-Axis:* Energy (Intensity).
    * *Insight:* Maps songs into emotional quadrants (Euphoria, Calm, Sadness, Anger).
* **Attribute Radar:** Compares the user's average `Danceability`, `Acousticness`, and `Speechiness` against the Global Dataset average.

### 5.3 Machine Learning Core (Backend)
* **Feature:** KNN Recommendation Engine.
* **Algorithm:** K-Nearest Neighbors (Scikit-Learn).
* **Input:** A "Seed Song" selected by the user (or their history average).
* **Process:** Calculates Euclidean distance in an n-dimensional vector space (audio features).
* **Output:** The 5 mathematically closest songs.

### 5.4 AI Agent (GenAI Integration)
* **Feature:** "The Music Psychologist."
* **Technology:** LLM API Integration (OpenAI GPT-4o / Gemini / DeepSeek).
* **Workflow:**
    1.  Backend calculates aggregate stats (e.g., "80% Depressing, Top Genre: Shoegaze").
    2.  **Prompt Engineering:** *"Act as a snobbish music critic and give opinions about this user's taste..."*
    3.  Frontend displays the generated response as rich text.

---

## 6. Non-Functional Requirements
* **Performance:** The `DataLoader` utility must load the CSV into memory (Singleton pattern) upon Django startup to avoid disk I/O latency on every request. Response times < 200ms.
* **Security:** LLM API Keys must reside in `.env` and never be exposed to the React Client.
* **Architecture:** Strict RESTful API. The Frontend must not be aware of the CSV logic; it should only consume standardized JSON.

---

## 7. Development Roadmap

* **Phase 1:** Infrastructure & Foundations (Completed).
* **Phase 2:** Data Engineering & ML Core (In Progress - Cleaning & KNN).
* **Phase 3:** API Services & AI Integration (Mock Auth & LLM).
* **Phase 4:** Frontend Visualization (React Charts).
* **Phase 5:** Production Polish & Deployment (Cloud).

---

## 8. Scope Analysis

### In Scope (MVP)
* CSV Dataset loading and EDA.
* Mock Authentication System.
* KNN Algorithm for "Similar Tracks."
* Basic LLM Integration (1 personality/prompt).
* Dashboard with 2 Key Charts (Radar & Scatter).

### Out of Scope (Future)
* In-app Audio Playback (Requires Spotify Premium SDK).
* Creating real Playlists on user account (Requires "Write" Scope).
* Native Mobile App (React Native).