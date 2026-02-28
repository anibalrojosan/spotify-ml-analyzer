# Product Roadmap: Spotify ML Analyzer

> **Current Status:** Phase 2: Simulation Core & Backend Logic
>
> **Last Updated:** 2026-02-28
>
> **Strategic Pivot:** Due to Spotify API verification blocks, the project is operating in **"Simulation Mode"** using static datasets until "Live Mode" (Phase 4) can be activated.

## Goal:
To build a resilient "Full Stack Data Science" application that delivers psychological insights from music data, regardless of live API availability.

## Execution Timeline

### Phase 1: Foundations (Done) 
- [x] **Project Scaffolding:** Initialized Django (Backend) and React (Frontend) monorepo structure.
- [x] **Environment:** Configured Docker, Git, and Virtual Environments.

### Phase 2: Simulation Core & Backend Logic (CURRENT)

#### 2.1 Data Science Layer (Done)
- [x] **Data Acquisition:** Sourced and cleaned Kaggle dataset (`cleaned_dataset.csv`).
- [x] **EDA:** Validated data quality and feature distributions.
- [x] **Archetype Definition:** Defined 5 User Personas (e.g., "The High Intensity", "The Organic") using K-Means Clustering.

#### 2.2 Backend Simulation Service (In Progress)
- [ ] **CSV Data Loader:** Implement `utils/data_loader.py` to ingest the dataset into Pandas/Memory (Singleton Pattern).
- [ ] **Mock Auth System:** Implement `MockAuthView` to bypass OAuth and assign a fake "User Archetype" session.
- [ ] **Profile Simulation:** Logic to generate a fake "Recently Played" history consistent with the assigned Archetype.

#### 2.3 Intelligence Services (Next Up)
- [ ] **Recommendation Engine:** Implement KNN endpoint (`/api/recommend`) to find nearest neighbors in the n-dimensional audio space.
- [ ] **AI "Psychologist":** Integrate Gemini/LLM API to interpret user stats and generate text-based personality insights.

### Phase 3: Frontend Visualization
- [ ] **Mock Connection:** Wire up the React Login button to the `MockAuthView` (Task: `Phase 2-05`).
- [ ] **Dashboard Implementation:** Build Radar Charts and Scatter Plots using Recharts/D3.
- [ ] **State Management:** Implement UserContext to hold the "Mock User" profile.

### Phase 4: The "Live" Switch (BLOCKED)
- [ ] **Spotify App Registration:** Verify Client ID/Secret.
- [ ] **Live OAuth 2.0:** Replace Mock Auth with real Spotify Handshake.
- [ ] **PostgreSQL Sync:** Replace CSV Loader with live ETL pipelines to DB.


## Strategic Notes
* **Architecture Mismatch:** The current `ARCHITECTURE.md` describes the *Phase 4 (Live)* system. I'm currently building a transient *Simulation Architecture* (In-Memory CSV) to maintain momentum.
* **Testing Strategy:** All backend logic is tested against the `cleaned_dataset.csv`, ensuring 100% reproducibility.