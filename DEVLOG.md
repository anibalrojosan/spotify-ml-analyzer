# 📝 Development Log

This document serves as a chronological record of the **Spotify ML Analyzer** development. Here, I document technical decisions, challenges faced, solutions, and lessons learned.

The goal is to maintain transparency throughout the process and generate a clear history of my "train of thought."

---

## [2025-12-26] - Step 0

**Focus:** Environment setup and architecture definition.

### Today's Objectives
1. Define the project structure (Monorepo).
2. Configure Git and ignore rules (`.gitignore`) for a hybrid environment (Python/Node).
3. Establish the initial Roadmap following the "Walking Skeleton" strategy.

### Technical Decisions
* **Monorepo Architecture:** I decided to keep the Backend (`django`) and Frontend (`react`) within a single repository. Although they might be deployed separately in production, keeping them together facilitates local development and API type management at this MVP stage.
* **Branching Strategy:** I will use a simplified Git Flow strategy. `main` for production/stable code, and `feat/...` or `fix/...` branches for every ticket in the Kanban board.

### Progress
- Repository initialized and connected to GitHub.
- `.gitignore` file configured to avoid uploading sensitive files (`.env`) or heavy dependencies (`node_modules`, `venv`).

### Next Steps
- Initialize the Django and React (Vite) projects.
- Successfully run both servers simultaneously on my local machine.

---

## [2025-12-26] - Day 1: Walking Skeleton

**Focus:** Backend and Frontend environment installation (Issue #2).

### Progress
- Successfully initialized the Django project using `uv`.
- Created the React frontend using Vite.
- **Milestone Reached:** Both servers (Django at port 8000 and React at port 5173) are running simultaneously. The "Walking Skeleton" is done!

### Challenges & Solutions
* **Node.js Version Conflict:**
    * **The Problem:** While setting up the frontend, `npm run dev` failed. The default Linux repository provided Node v18.19.1, but the latest version of Vite requires Node v20+ or v22+.
    * **The Fix:** Instead of relying on the system's `apt` package manager, I installed **NVM (Node Version Manager)** so I can install Node v22 cleanly without sudo permissions.
    * **Lesson:** Always check engine requirements for modern frontend tools; system defaults may be outdated.

---

## [2025-12-29]

**Focus:** Data Acquisition Strategy & Initial EDA Pipeline

### Progress:
- Data Source: Acquired a comprehensive dataset of ~30,000 Spotify tracks to serve as a local development proxy.
- Data Cleaning: Implemented cleaning logic using Pandas, specifically addressing duplicates and null values to ensure data integrity.
- EDA: Started Exploratory Data Analysis to understand feature distributions (valence, energy, etc.) before modeling.

### Challenges & Solutions:
- **Challenge:** Encountered authentication blockers with the Spotify for Developers API, which halted the backend integration.
- **Solution (Pivot):** Adopted a "Local Simulation" strategy. Instead of waiting on the API, I decided to use a static dataset to mock API responses. This allows the Data Science work to proceed in parallel while the authentication issues are resolved.

---

## [2025-12-30]

**Focus:** Psychometric validation & Dimensional reduction
### Progress: 
- **Statistical Sanity Check**: Computed correlation matrices to identify multicollinearity. Confirmed that Valence and Energy are orthogonal (independent) dimensions in this dataset, validating their use as separate axes.
- **Affective Mapping**: Implemented Russell’s Circumplex Model, plotting 30k tracks on the Valence-Energy plane to visualize emotional quadrants.
- **Genre Clustering (Attempt 1)**: Visualized genre centroids to test if genre labels could predict emotional states. (Preliminary results suggest significant overlap).

---

## [2026-01-01]

**Focus**: Variance analysis & Backend rule definition
### Progress:
- **Distribution Profiling**: Transitioned from centroid analysis to **Boxplot Distribution** analysis. Examined the variance of Valence, Energy, and Tempo across genres.
- **Key Architectural Insight**: Discovered that mainstream genres (Pop, Latin) have high variance in emotional features, making them poor predictors of mood. Conversely, genres like EDM and Rock showed high rigidity in intensity.
- **Backend Specification**: Defined the logic for the **Psychological Profile Engine**:
    - Mood: Must be calculated at the **Track-Level** (atomic).
    - Intensity: Can use Genre-Level heuristics (e.g., EDM implies High Energy).

---

## [2026-01-02]

**Focus**: Unsupervised Learning setup & Architecture research

### Progress:

* **Architecture Research**: Investigated **Decoupled Client-Server Architecture** patterns. Confirmed the strategy to use Django as a pure REST API provider serving JSON and React as a standalone consumer, ensuring separation of concerns between Data Science logic and UI.
* **EDA Pivot**: Shifted focus from descriptive statistics to **Unsupervised Machine Learning**. Prepared the dataset for clustering by removing noise and applying `StandardScaler` to normalize audio features (loudness, tempo, energy).
* **K-Means Initialization**: Implemented the **Elbow Method** to determine the optimal number of clusters. Analyzed inertia plots to identify potential inflection points between 4 and 6 clusters.

## [2026-01-03]

**Focus**: Clustering Model Finalization & Archetype definition

### Progress:

* **Model Selection**: Finalized the K-Means training and analysis. Evaluated performance using **Silhouette Score** and **Davies-Bouldin Index**, determining that 5 clusters offered better separation and psychological interpretability than 4 or 6.
* **Feature Interpretation**: Used **PCA (Principal Component Analysis)** to visualize high-dimensional data in 2D. Identified PC1 as the "Intensity Spectrum" (Organic vs. Synthetic) and PC2 as the "Mood Spectrum" (Introspective vs. Social).
* **Profile Definition**: Mapped the 5 clusters to specific backend archetypes: *The Organic/Relaxed*, *The Euphoric/Social*, *The High Intensity*, *The Rhythmic Flow*, and *The Mainstream Groove*.
* **Code Refactoring**: Split the monolithic EDA notebook into `2.0-eda-mood-distribution` and `3.0-model-clustering-profiles`.

## [2026-01-05] Project Planning & Requirements Definition

**Focus**: Researching best practices for project documentation and drafting the Product Requirements Document (PRD).

### Progress:
* **Documentation Research**: Conducted an analysis of industry-standard planning documents to ensure a structured development lifecycle.

* **Drafted the initial (PRD)**. This included:

    * Defining the core problem and solution.

    * Establishing the MVP scope to prevent scope creep.

    * Outlining user stories and acceptance criteria.

**Goal**: To establish a clear roadmap and functional specifications before the engineering phase begins.