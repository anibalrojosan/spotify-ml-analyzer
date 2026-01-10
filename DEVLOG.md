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

## [2026-01-06] Project Requirements Document & Technical Design Document

**Status:** 🟢 Planning & design completed

Today was entirely dedicated to moving from "abstract ideas" to a concrete engineering plan. Before continue writing production code, I wanted to ensure the architecture could handle the specific constraints of this project (latency, API limits, and the simulation phase).

### Key Achievements

1.  **Product Requirements Document (PRD) finalized:**
    * Defined the scope of the MVP.
    * Clarified the "Simulation Strategy": Since I don't have Spotify API access yet, I formally documented the pivot to using a **Kaggle Dataset** for the initial development phase.
    * Established the core value proposition: **K-Means Clustering** (Math) + **LLM Analysis** (Psychology).

2.  **Technical Design Document (TDD) created and finalized:**
    * This was the heavy lifting of the day. I chose a **Synchronous Monolithic Architecture** using Django.
    * **Crucial Decision:** To avoid HTTP timeouts (since ML and OpenAI calls are slow), I designed a **"Store-First, Analyze-Later"** pattern.
        * Endpoint A (`/sync`): Fetches data and saves to DB (Fast).
        * Endpoint B (`/report`): Reads local DB and runs K-Means (Safe).

3.  **Visualizing the Architecture (Mermaid.js):**
    * Created the Sequence Diagrams to map the split data flow.
    * Designed the Entity-Relationship Diagram (ERD), adding a `UserInsight` table to cache the expensive LLM responses.
    * *Lesson Learned:* Mermaid diagrams render differently on GitHub vs. local editors. I decided to export high-res PNGs for the README and docs to ensure consistency.

4.  **README Overhaul:**
    * Updated the public documentation to reflect the technical reality.
    * Added the new architecture diagrams and clarified the roadmap phases (Offline vs. Live).

### Technical Takeaway
It's tempting to jump straight into coding `views.py`, and continue coding indefinely, but the complexity of the project and all it's layers make difficult to have a clear view of what things needs to be done and when (earlier or after another features). Writing the **TDD** first saved me from a future headache. I almost designed a single blocking endpoint that would have definitely crashed the browser on slow networks. Splitting the logic into **ETL** vs **Inference** phases at the design stage was a win. From now on I have these documents as a quick reference that allows a clearer view of what needs to be built.

## [2026-01-06]  Stopping to Check the Roadmap

**Status:** Strategy Alignment

Before developing the app further i wanted to slow down to have a clearer view of whats next.

As I dove deeper into the **Phase 2** development (building the Mock Simulation Engine), I realized a dangerous ambiguity was forming. My Architecture document (`TDD`) described a "Live" system connected to Spotify's API and PostgreSQL, but my current reality is a "Simulation" system running off a static CSV due to API blocks. Also this confused me on what nexts steps were the correct ones, and what needs to be tackled now. Working without acknowledging this discrepancy is how technical debt is born.

As time passes, the issues that I had set seems not so clear anymore ("why I chose to do those tasks next?). So I needed an 'update' on these issues.

**What I did today:**
I paused development to consolidate my PRD, Architecture, and GitHub Issues into a single "Source of Truth": the **`ROADMAP.md`**.

**Why this matters:**
* **Architecture Honesty:** The Roadmap now explicitly splits the project into "Simulation Mode" (Current) and "Live Mode" (Future). This gives me permission to write "Throwaway Code" (like the CSV Loader) without feeling guilty that it doesn't match the final architecture.
* **Mental Clarity:** Instead of holding the entire plan in my head or on disperse notes, I have a document that tells me exactly what "Done" looks like for Phase 2.
* **Prioritization:** The "Real Spotify Auth" was moved to the Icebox (Phase 4). Now, the path to the MVP is unblocked.

**Takeaway:**
Coding it's not so hard. But it takes a lot of attention that quickly disolves the greater picture. A clear direction, and mantain clarity about it is hard. So a ROADMAP comes very handy for later planning.

**Next Up:**
Continue with Phase 2. Start with Task **2.2 Backend Simulation Service**.

## [2026-01-10] Building the simulation engine (Backend Layer)

**Status:** Backend implementation

After defining the Roadmap, it was time for execution. I successfully implemented the core simulation logic that allows the app to function without the live Spotify API.

**What I built:**
* **The Data Engine:** Implemented `SpotifyDataLoader` in `utils/`.
    * *Technical Detail:* Used the **Singleton Pattern** and Lazy Loading to ingest the 30k row CSV into memory only once. This prevents disk I/O bottlenecks on every request.
* **The Mock Auth System:** Created the `MockAuthView` endpoint (`POST /api/auth/login/`).
    * Instead of a simple "Success", this view acts as a **User Factory**. It assigns one of the **5 User Archetypes** (defined in the Clustering analysis).
    * *Feature:* I added logic to force a specific archetype via `request.data` (e.g., `{"archetype_id": 1}`). This makes the system **Deterministic for Testing** but **Random for Demoing**.
* **API Plumbing:** Configured `django.urls` to expose the API.

**Verification:**
Validated the endpoint using `curl`. The server now responds with a structured JSON containing a fake User Profile and Access Token, mimicking the real Spotify response structure.

**Next Up:**
The Backend is ready. Now it's time to tackle the Frontend.