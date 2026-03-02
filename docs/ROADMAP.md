# Product Roadmap: Spotify ML Analyzer

> **Current Status:** Phase 2: The Simulation Engine (Data Layer)
>
> **Last Updated:** 2026-03-02
>
> **Strategic Pivot:** Operating in **"Simulation Mode"** using static datasets and a PostgreSQL-first approach to ensure a seamless transition to "Live Mode" (Phase 5).

## Goal:
To build a resilient "Full Stack Data Science" application that delivers psychological insights from music data, regardless of live API availability.

## Execution Timeline

### Phase 1: Foundations & Research (Done)
- [x] **Project Scaffolding:** Initialized Django (Backend) and Next.js (Frontend) structure.
- [x] **Data Science Layer:** Sourced Kaggle dataset, performed EDA, and defined 5 User Archetypes using K-Means.
- [x] **Environment:** Configured Docker, Git, and Virtual Environments.

### Phase 2: Simulation Engine (CURRENT)
- [ ] **Database Schema:** Define Django Models for `Track`, `AudioFeatures`, and `UserArchetype`.
- [ ] **Unified Ingestor:** Implement `CSVIngestor` as a Django Management Command to populate PostgreSQL from CSV.
- [ ] **Mock Auth System:** Implement `MockAuthView` to assign a fake "User Archetype" session.
- [ ] **Profile API:** Endpoints to retrieve tracks and features consistent with the assigned Archetype.

### Phase 3: Visual Prototype & UX Validation
- [ ] **Next.js Dashboard:** Build the core layout and navigation.
- [ ] **Data Visualization:** Implement **Radar Charts** (audio features) and **Scatter Plots** using Recharts.
- [ ] **State Management:** Implement `UserStore` with Zustand to handle simulation sessions.

### Phase 4: Intelligence & Insights
- [ ] **Recommendation Engine:** Implement `/api/recommend` using pre-trained KNN models (Scikit-learn).
- [ ] **AI Psychologist:** Integrate **Google Gemini API** to generate personality insights based on dashboard data.
- [ ] **Insight UI:** Build the "Psychological Profile" view with AI-generated text.

### Phase 5: Creating the Live Switch (Blocked)
- [ ] **Spotify OAuth 2.0:** Replace Mock Auth with real Spotify Handshake.
- [ ] **Live ETL Pipeline:** Implement `SpotifyAPIIngestor` to sync live user data into the existing DB schema.
- [ ] **Production Deployment:** Finalize Railway configuration for live traffic.

## Strategic Notes
*   **DB-First Approach:** We use PostgreSQL from Phase 2 to avoid refactoring when switching from CSV to API.
*   **Decoupled Intelligence:** The AI and Recommendation logic are built on top of the DB schema, making them source-agnostic.
*   **Early Visualization:** Phase 3 ensures we validate the UX and data story before adding expensive AI calls.
