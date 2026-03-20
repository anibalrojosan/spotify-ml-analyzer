# 📝 Development Log

This document serves as a chronological record of the **Spotify ML Analyzer** development. Here, I document technical decisions, challenges faced, solutions, and lessons learned.

The goal is to maintain transparency throughout the process and generate a clear history of my "train of thought."


## Index

* [**[2026-03-20]** - Phase 2-04: Declaring API Contract with the Frontend in Simulation Mode](#2026-03-20---phase-2-04-declaring-api-contract-with-the-frontend-in-simulation-mode)
* [**[2026-03-20]** - REVIEW: N+1 Query Problem & Bulk Operations](#2026-03-20---review-n1-query-problem--bulk-operations)
* [**[2026-03-18]** - Refactor: Massive Performance Optimization for CSV Ingestion](#2026-03-18---refactor-massive-performance-optimization-for-csv-ingestion)
* [**[2026-03-17]** - REVIEW: Django Rest Framework (DRF)](#2026-03-17---review-django-rest-framework-drf)
* [**[2026-03-17]** - Phase 2-03: Mock Authentication & Archetype Provider](#2026-03-17---phase-2-03-mock-authentication--archetype-provider)
* [**[2026-03-16]** - Phase 2-02: CSV Data Ingestion & Archetype Seeding](#2026-03-16---phase-2-02-csv-data-ingestion--archetype-seeding)
* [**[2026-03-10]** - Phase 2-01: Relational Schema & Infrastructure Setup](#2026-03-10---phase-2-01-relational-schema--infrastructure-setup)
* [**[2026-03-02]** - Architecture Finalization and Frontend Pivot](#2026-03-02---architecture-finalization-and-frontend-pivot)
* [**[2026-02-28]** - Project Refactoring and Dependency Migration](#2026-02-28---project-refactoring-and-dependency-migration)
* [**[2026-01-06]** - Stopping to Check the Roadmap](#2026-01-06---stopping-to-check-the-roadmap)
* [**[2026-01-06]** - Project Requirements Document & Technical Design Document](#2026-01-06---project-requirements-document-and-technical-design-document)
* [**[2026-01-05]** - Project Planning & Requirements Definition](#2026-01-05---project-planning-and-requirements-definition)
* [**[2026-01-03]** - Clustering Model Finalization & Archetype definition](#2026-01-03---clustering-model-finalization-and-archetype-definition)
* [**[2026-01-02]** - Unsupervised Learning setup & Architecture research](#2026-01-02---unsupervised-learning-setup-and-architecture-research)
* [**[2026-01-01]** - Variance analysis & Backend rule definition](#2026-01-01---variance-analysis-and-backend-rule-definition)
* [**[2025-12-30]** - Psychometric validation & Dimensional reduction](#2025-12-30---psychometric-validation-and-dimensional-reduction)
* [**[2025-12-29]** - Data Acquisition Strategy & Initial EDA Pipeline](#2025-12-29---data-acquisition-strategy-and-initial-eda-pipeline)
* [**[2025-12-26]** - Day 1: Walking Skeleton](#2025-12-26---day-1-walking-skeleton)
* [**[2025-12-26]** - Step 0](#2025-12-26---step-0)

---

## [2026-03-20] - Phase 2-04: Declaring API Contract with the Frontend in Simulation Mode

### Context & Goals
While working on **Phase 2-04** (`feat/api-profile-endpoints`), the mock stack from **Phase 2-03** (`MockSessionAuthentication`, `MockLoginView`, `MeView`, serializers) was easy to lose track of across files. I decided to formalize the API contract with the frontend in simulation mode. The frontend needs a **single, explicit contract** for simulation mode—URLs, JSON shapes, cookie/session behavior, and how `request.user` is populated—without reading Django settings and DRF internals each time. The goal was to capture those decisions in one document before implementing `/api/profile/...`.

### Technical Implementation
- **New documentation:** Added `docs/Frontend/API_CONTRACT.md` as the canonical reference for simulation-mode API consumption.
- **Navigation:** Included a table of contents with stable HTML anchors, relative links to backend sources (`authentication.py`, `views.py`, `serializers.py`, `models.py`, `urls.py`, `settings.py`, `seed_archetypes.py`), and links to this DEVLOG.
- **Diagrams:** Embedded three **Mermaid** diagrams—component flow (request -> session -> auth -> `UserSerializer`), sequence (`POST /api/auth/mock-login/` then `GET /api/auth/me/`), and the `/me/` 401 decision path.
- **Contract tables:** Documented HTTP methods/paths and the `User` / nested `Archetype` JSON fields aligned with `UserSerializer` and `ArchetypeSerializer`, including what is intentionally *not* exposed (`min_values` / `max_values` on auth responses).
- **Operational checklist:** Frontend-focused items (`credentials: 'include'`, hydrate via `/me/`, QA slug override).

### 💡 Deep Dive: Documentation as the Integration Boundary

An **API contract** document is not a substitute for OpenAPI or tests, but it fixes the *social* boundary between backend and frontend: it states what the client may rely on (field names, auth mechanism, error shape) versus what is implementation detail (ORM layout, session key names inside Django). For mock mode, that boundary matters because:
- `request.user` is a **`UserProfile`**, not `django.contrib.auth.models.User`
- Persistence is a **session cookie**, not a Bearer token

Writing that down reduces regressions when Phase 2-04 adds profile endpoints: new serializers can extend the API Contract document under a “Profile API” section without rewriting the auth narrative.

### Next Steps
- Continue with the implementation of **Phase 2-04** endpoints (`GET /api/profile/summary/`, `GET /api/profile/tracks/`) and extend `API_CONTRACT.md` with their schemas and latency notes.

---

## [2026-03-20] - Review: N+1 Query Problem & Bulk Operations

### Context & Goals
Before continue with the phase 3 of this project, I decided to review the N+1 query problem presented in the `ingest_tracks` management command. The goal of this entry is to document why the anti-pattern emerged, which tools contributed to it (e.g., Pandas `iterrows()`, sequential `for` loops with ORM calls), and how it was solved using Django's bulk operations and in-memory data preparation.

### Technical Implementation
- **Root Cause Analysis:** The N×4 problem arose from combining `chunk.iterrows()` (row-by-row iteration) with `update_or_create()` inside the loop—each row triggered 4 SQL queries.
- **Solution Pattern:** Separate data preparation (in memory) from database writes (bulk operations).
- **Django ORM Tools Used:** `bulk_create()`, `update_conflicts=True`, `filter(spotify_id__in=...)` for batch retrieval.

### 💡 Deep Dive: N+1 Problem, Its Causes, and the Bulk Solution

#### 1. What is the N+1 Problem?
The N+1 query problem occurs when the code executes **1 initial query** to fetch a list of objects, and then **N additional queries**—one per object—to fetch related data. The name comes from the total of queries: 1 + N queries.

In my case, I had a **write-side variant**: instead of N+1 reads, I had **N×4 writes**—4 queries per row (2 for `Track`, 2 for `AudioFeatures` via `update_or_create`).

#### 2. Why Did My Script Generate It?

**2.1 Pandas `iterrows()`**
I used `chunk.iterrows()` to iterate over each row of the DataFrame:

```python
for _, row in chunk.iterrows():
    # ...
```

- `iterrows()` returns `(index, Series)` per row. Each `Series` is a new object, which adds overhead (extra memory usage and CPU time that does not contribute to the final result).
- The loop is inherently **row-by-row** and sequential. Any database call inside this loop runs once per row.
- Pandas docs warn that `iterrows()` is slow; for my use case, the main issue was not `iterrows()` itself but the **database calls inside the loop**.

**2.2 The `for` Loop + ORM Anti-Pattern**
The code I was using looked like this:

```python
for _, row in chunk.iterrows():
    with transaction.atomic():
        track, created = Track.objects.update_or_create(spotify_id=spotify_id, defaults=track_data)  # 2 queries
        AudioFeatures.objects.update_or_create(track=track, defaults=features_data)  # 2 queries
```

- `update_or_create` does a `SELECT` to check existence, then an `INSERT` or `UPDATE`—2 queries per call.
- With 2 models, that's **4 queries per row**.
- For 1000 rows: **4000 sequential SQL queries** per chunk.

**2.3 Transaction Overhead**
`transaction.atomic()` was inside the loop, so I opened and committed a transaction for every row instead of once per chunk.

#### 3. Solution with `bulk_create` and `update_conflicts`

**3.1 In-Memory Preparation (No Database Calls)**
The refactored loop only builds Python objects and stores them in lists/dicts without touching the database:

```python
tracks_to_create = []
features_data_map = {}  # spotify_id -> features_data
seen_spotify_ids = set()

for _, row in chunk.iterrows():
    # ... extract track_data, spotify_id, features_data ...
    if spotify_id in seen_spotify_ids:
        continue
    seen_spotify_ids.add(spotify_id)

    track = Track(spotify_id=spotify_id, **track_data)
    tracks_to_create.append(track)
    features_data_map[spotify_id] = features_data
```

No `update_or_create`, no `save()`, no queries, only in-memory preparation.

**3.2 Bulk Upsert of Tracks**
All tracks in the chunk are sent in a single SQL statement:

```python
Track.objects.bulk_create(
    tracks_to_create,
    update_conflicts=True,
    unique_fields=['spotify_id'],
    update_fields=['title', 'artist_name', 'album_name']
)
```

PostgreSQL executes something like:

```sql
INSERT INTO api_track (spotify_id, title, ...) VALUES (...), (...), (...)
ON CONFLICT (spotify_id) DO UPDATE SET title = EXCLUDED.title, ...
```

**3.3 Retrieve Track IDs for Foreign Keys**
`AudioFeatures` needs the database `id` of each `Track`. I fetched them in one query using the `__in` lookup:

```python
spotify_ids = list(features_data_map.keys())
tracks_db = Track.objects.filter(spotify_id__in=spotify_ids)
```

- `spotify_id__in` uses Django's lookup syntax: `__` separates field and lookup; `in` maps to SQL `IN (...)`.
- One `SELECT` returns all matching tracks with their UUIDs.

**3.4 Bulk Upsert of AudioFeatures**
I built `AudioFeatures` instances and inserted them in one call:

```python
features_to_create = []
for track_db in tracks_db:
    f_data = features_data_map[track_db.spotify_id]
    features_to_create.append(AudioFeatures(track=track_db, **f_data))

AudioFeatures.objects.bulk_create(
    features_to_create,
    update_conflicts=True,
    unique_fields=['track'],
    update_fields=list(self.FEATURES_MAP.values())
)
```

**Summary:** 3 queries per chunk instead of 4000—roughly 28× faster in my tests.

### Next Steps
- Consider replacing `iterrows()` with `itertuples()` or vectorized operations if row iteration remains a bottleneck.
- Apply this bulk-processing pattern to future ingestion or batch jobs.

---

## [2026-03-18] - Refactor: Massive Performance Optimization for CSV Ingestion

### Context & Goals
The initial implementation of the `ingest_tracks` management command was functional but highly inefficient. It processed the Kaggle CSV dataset by iterating through rows sequentially and hitting the database multiple times per row using `update_or_create`. While the dataset 'only' has ~30.000 rows, this caused severe performance bottlenecks, taking approximately 17 seconds per 1000 records. Extrapolated to a million row dataset, the job would take over 4 hours and likely crash due to memory exhaustion or database connection timeouts. The goal was to refactor the ingestion logic to process data in true batches, minimizing database queries and execution time.

### Technical Implementation
- **Removed Sequential DB Calls:** Eliminated the use of `update_or_create` inside the `for` loop in `backend/api/management/commands/ingest_tracks.py`.
- **In-Memory Preparation:** Refactored the loop to only instantiate `Track` and `AudioFeatures` objects in Python's RAM, storing them in lists and dictionaries without touching the database.
- **In-Chunk Deduplication:** Added a `Set` to track `spotify_id`s within the same chunk to prevent `IntegrityError` during bulk inserts if the CSV contained duplicate rows close to each other.
- **Bulk Operations:** Implemented Django's `bulk_create` with `update_conflicts=True` to perform true UPSERT operations at the database level.
- **Empirical Results:** The refactor reduced the processing time from ~17.0s per chunk to ~0.6s per chunk, making the script approximately **28 times faster**.

### 💡 Deep Dive: The N x 4 Problem vs. Bulk Upserts
The original implementation suffered from a severe anti-pattern similar to the N+1 query problem, but for writes. For every single row in the CSV, Django's `update_or_create` executed two queries (a `SELECT` to check existence, then an `INSERT`/`UPDATE`). Since there are two models (`Track` and `AudioFeatures`), processing a chunk of 1000 rows resulted in **4000 sequential SQL queries**. The latency of waiting for the database to respond 4000 times per chunk is what killed the performance.

The refactored approach uses a **3-query pattern per chunk**, regardless of the chunk size:
1. **`Track.objects.bulk_create(..., update_conflicts=True)`**: Sends all 1000 tracks in a single `INSERT INTO ... ON CONFLICT DO UPDATE` statement.
2. **`Track.objects.filter(spotify_id__in=...)`**: A single `SELECT` to retrieve the actual database `id`s (UUIDs) assigned to those tracks, which are needed for the foreign key relationship.
3. **`AudioFeatures.objects.bulk_create(...)`**: A final massive `INSERT` statement for all the related features.

By shifting the workload from Python's sequential loops to PostgreSQL's optimized bulk processing capabilities, this refactor drastically reduced network I/O and transaction overhead.

### Next Steps
- Continue with Phase 3 development (Frontend integration).
- Ensure future background jobs follow this bulk-processing pattern to prevent OOM (Out of Memory) errors in production.

---

## [2026-03-17] - Review: Django Rest Framework (DRF)

To implement **Phase2-03** I reviewed the Django Rest Framework (DRF) documentation and implemented the mock authentication system and the archetype provider to unblock frontend development and simulate user sessions.

DRF it's a library on top of Django that helps to build RESTful APIs quickly and easily. The main idea it's to create a RESTful API layer that communicates the Django's Backend (models and views) with a independent frontend that can be used by any client, using JSON as a communication protocol.

Fundamental concepts learned that I had to review were:

1. **Serializers (The Translation Layer):**
   - **Concept:** Act as a bridge between complex Django Model instances and flat JSON data. They are used to convert the Django models (Python code) into JSON data that can be used by the frontend.
   - **Implementation:** Used `ModelSerializer` for `UserArchetype` and `UserProfile` to automatically map database fields.
   - **Advanced usage:** Implemented `SerializerMethodField` to create `avatar_url`. This is a "read-only" field that doesn't exist in the DB but is calculated on-the-fly via a `get_avatar_url` method, allowing us to integrate external services like DiceBear API seamlessly.

2. **Authentication Classes (The Identity Layer):**
   - **Concept:** Determine *who* is making the request. DRF allows multiple strategies (Session, Token, JWT).
   - **Implementation:** Created a custom `MockSessionAuthentication`. This was necessary because our `UserProfile` is a custom model that doesn't inherit from Django's built-in `User`. The class reads the `user_id` from the Django session and "injects" the corresponding profile into `request.user`.

3. **Permission Classes (The Security Layer):**
   - **Concept:** Determine *if* the identified user has the right to perform an action.
   - **Implementation:** Used `IsAuthenticated` in the `MeView`. This class checks if `request.user` exists and if its `is_authenticated` property is `True`. To make this work with our custom model, I had to add a `@property is_authenticated` to the `UserProfile` model.

**Key Takeaway:** DRF's power lies in its modularity. By separating *how we translate data* (Serializers) from *how we identify users* (Authentication) and *what they can do* (Permissions), an API can be created that is easy to test and ready to be swapped for "Real Spotify Auth" in the future without changing the business logic.

---

## [2026-03-17] - Phase 2-03: Mock Authentication & Archetype Provider

Today I implemented the mock authentication system and the archetype provider to unblock frontend development and simulate user sessions.

### Context & Goals
The goal was to create a "Simulation Mode" authentication that mimics the future Spotify OAuth flow. This allows the frontend to have a `request.user` object and a persistent session without needing real API credentials yet.

### Technical Implementation
- **Serializers:** Created `ArchetypeSerializer` and `UserSerializer` in `backend/api/serializers.py` to define the data contract for the frontend. A mock avatar URL using DiceBear API was created using a `SerializerMethodField`.
- **Mock Login Endpoint:** Implemented `MockLoginView` in `backend/api/views.py` which allows selecting an archetype and establishes a Django session.
- **Custom Authentication:** Created `MockSessionAuthentication` in `backend/api/authentication.py`. This class "injects" the `UserProfile` into `request.user` if a valid session exists.
- **User Verification:** Added a `MeView` (`/api/auth/me/`) to allow the frontend to verify the current session state.
- **Model Enhancement:** Added `is_authenticated` property to `UserProfile` to satisfy Django Rest Framework's permission system.

### 💡 Deep Dive: Django Rest Framework (DRF)
DRF was used to build the API layer. Key concepts applied:
- **Serializers:** Act as a translation layer between complex Django models and JSON. We used `SerializerMethodField` for dynamic data like avatars.
- **Authentication Classes:** We bypassed the default `SessionAuthentication` with a custom one to map our `UserProfile` (which doesn't inherit from Django's `User`) to `request.user`.
- **Permission Classes:** Used `IsAuthenticated` to protect the `/me/` endpoint, ensuring only users with an active mock session can access it.

### Next Steps
- Implement track filtering logic based on the assigned `UserArchetype` (Phase 2-04).
- Create the simulation dashboard in the frontend to visualize the assigned profile.

---

## [2026-03-16] - Phase 2-02: CSV Data Ingestion & Archetype Seeding

Focused on populating the database with the Kaggle dataset and the predefined psychological archetypes.

### Context & Goals
To run the simulation, I needed a local database filled with tracks and their audio features. Additionally, I needed to materialize the 5 archetypes identified in the clustering phase into the database.

### Technical Implementation
- **CSV Ingestor:** Developed `ingest_tracks` management command. It processes the Kaggle CSV in chunks (1000 rows) to maintain a low memory footprint.
- **Data Integrity:** Implemented `update_or_create` logic to ensure idempotency and avoid duplicate tracks or features.
- **Archetype Seeding:** Created `seed_archetypes` command to populate the `UserArchetype` model with the 5 clusters (Organic, Euphoric, High Intensity, Rhythmic, Mainstream) and their defining feature ranges.
- **Logging:** Added a local `ingestion_log.txt` to track progress and errors during long-running imports.

### 💡 Deep Dive: Management Commands vs. Django Admin
While the Django Admin is great for manual edits, I chose to use **Management Commands** for data population for several reasons:
- **Automation:** Scripts can be version-controlled and executed as part of a CI/CD pipeline or environment setup.
- **Performance:** Using `bulk_create` or chunked processing is significantly faster than manual entry.
- **Repeatability:** Ensures that every developer involved in a project has the exact same set of data (tracks and archetypes) in the database.

### Next Steps
- Implement the Mock Authentication system to link users with these archetypes.
- Setup DRF serializers to expose this data via API.

---

## [2026-03-10] - Phase 2-01: Relational Schema & Infrastructure Setup

After finishing the enhancements of the documentation, I continued with Phase 2. Today's sprint was focused on setting up the database schema and the infrastructure.

### Context & Goals
The primary goal of this sprint was to transition from a conceptual architecture to a functional data persistence layer. I needed to establish a robust PostgreSQL foundation capable of handling both the current **Simulation Mode** (Kaggle dataset) and the future **Live Mode** (Spotify API), ensuring data integrity and scalability from the start.

### Technical Implementation
- **Infrastructure:** Configured `docker-compose.yml` with **PostgreSQL 18-alpine** on a custom port (`5435`) to avoid local conflicts.
- **Environment Management:** Implemented `.env` and `.env.example` pattern using `python-dotenv` for secure credential handling.
- **Database Schema:** Defined core models in `backend/api/models.py`:
    - `Track`: Central entity with indexed `spotify_id` for fast lookups.
    - `AudioFeatures`: 1:1 relationship with `Track` to isolate numerical ML data.
    - `UserArchetype`: Template for simulated user profiles using `JSONField`.
    - `UserProfile` & `UserInsight`: Entities for session persistence and AI-generated report storage.
- **Documentation:** Created `docs/DATABASE.md` (ERD) and `docs/CLASS_DIAGRAM.md` using Mermaid.js to ensure architectural alignment.
- **Admin Interface:** Registered all models in `api/admin.py` with custom `list_display`, `search_fields`, and `list_filter` for efficient data inspection.
- **Migrations:** Successfully executed `makemigrations` and `migrate` to materialize the schema in PostgreSQL.

### 💡 Deep Dive: Advanced Django Model Fields
To ensure the system is both flexible and performant, we utilized several specialized Django ORM features:
- **`UUIDField`**: Used for primary keys to provide non-sequential, globally unique identifiers, enhancing API security and data portability.
- **`JSONField`**: Implemented in `UserArchetype` and `UserInsight`. This allows storing unstructured data (like ML centroids or dynamic filtering ranges) directly in PostgreSQL as `jsonb`, providing NoSQL-like flexibility within a relational database.
- **`OneToOneField` vs `ForeignKey`**: Used `OneToOneField` for `AudioFeatures` to enforce strict data integrity (one track = one set of features), while `ForeignKey` was used for `UserArchetype` to allow multiple users to share the same musical profile.
- **`db_index=True`**: Applied to `spotify_id` to create a B-Tree index in PostgreSQL, which is critical for the upcoming `CSVIngestor` performance.

### Next Steps
- Implement the `CSVIngestor` management command (Sprint `phase2-02`) to populate the database with the Kaggle dataset.
- Develop the Mock Authentication provider to simulate user sessions based on Archetypes.
- Create the first set of REST API endpoints to expose track data to the Frontend.

---

## [2026-03-02] - Architecture Finalization and Frontend Pivot

**Status:** Planning & Documentation Completed

Today I finalized the technical planning for the next development phases, focusing on creating a robust and professional architecture. I focused mainly on drafting the ADRs and enhance the Roadmap. I had to take some decisions on how to how and when implmentedn the database schema and the frontend. and waht tools to use. This planning aims to make easier to continue with the development and avoid future refactoring (as it seems it was needed as the previous plan).

**What I did today:**
*   **Created ADRs 001-009:** Documented all major architectural decisions, including backend (Django), persistence (PostgreSQL), deployment (Railway), and intelligence (Gemini).
*   **Frontend Pivot (Next.js vs Streamlit):** Decided to use **Next.js + Shadcn/UI + Tailwind CSS** instead of Streamlit to avoid "throwaway code" and ensure a professional aesthetic from the start (ADR 009).
*   **State & Visualization:** Chose **Zustand** for lightweight state management and **Recharts** for interactive data visualizations (ADR 008).
*   **Unified Ingestion Strategy:** Defined a "Unified Ingestor" pattern (ADR 006) to handle both CSV (Simulation) and Spotify API (Live) data seamlessly.
*   **Roadmap Update:** Reorganized the `ROADMAP.md` into an agile, DB-first approach to minimize future refactoring.

**Why this matters:**
*   **Professionalism:** Moving away from Streamlit ensures the app looks like a real product, not a data science script.
*   **Maintainability:** The ADRs provide a clear "why" for every tool choice, making it easier to scale or pivot in the future.
*   **Efficiency:** The DB-first strategy ensures that the work done in Phase 2 (Simulation) is directly reusable in Phase 5 (Live).


## [2026-02-28] - Project Refactoring and Dependency Migration

**Status:** Infrastructure Optimization

Today I performed a significant cleanup of the project's infrastructure to improve development speed and maintainability. The focus was on migrating to more modern tooling and removing unused boilerplate code. As I reached the last steps of phase 2, I realized I needed to take a step back to align my thinking and the project's direction.

**What I did today:**
*   **Migrated from `pip` to `uv`:** Replaced `requirements.txt` with `pyproject.toml` and `uv.lock`. This transition significantly speeds up dependency resolution and provides a more robust environment management.
*   **Frontend Cleanup:** Deleted the default Vite/React boilerplate in the `frontend/` directory. Since it only contained example code, I decided to remove it to reduce noise and will recreate a clean version (likely using Next.js) when Phase 3 begins.
*   **Documentation Synchronization:** Updated `ARCHITECTURE.md`, `README.md`, and `ROADMAP.md` to reflect the current "Simulation Mode" strategy and the updated tech stack.
*   **Diagrams as Code:** Replaced static images in the architecture documentation with **Mermaid.js** diagrams for easier maintenance and version control.

**Why this matters:**
*   **Modern Tooling:** `uv` is much faster than `pip` and its lockfile ensures reproducibility across different environments (like WSL2 and production).
*   **Zero Noise:** Keeping the repository free of unused boilerplate code allows me to focus on the core logic of the ML engine without distractions.
*   **Living Documentation:** Using Mermaid ensures that architecture diagrams evolve alongside the code, preventing them from becoming obsolete.

**Next Up:**
- Further improvements to the documentation, especially the roadmap.
- Further improvements to the sprints and tasks planning.

## [2026-01-06] - Stopping to Check the Roadmap

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

## [2026-01-06] - Project Requirements Document & Technical Design Document

**Status:** 🟢 Planning & design completed

Today was entirely dedicated to moving from "abstract ideas" to a concrete engineering plan. Before continue writing production code, I wanted to ensure the architecture could handle the specific constraints of this project (latency, API limits, and the simulation phase).

### Key Achievements

1. **Product Requirements Document (PRD) finalized:**
* Defined the scope of the MVP.
* Clarified the "Simulation Strategy": Since I don't have Spotify API access yet, I formally documented the pivot to using a **Kaggle Dataset** for the initial development phase.
* Established the core value proposition: **K-Means Clustering** (Math) + **LLM Analysis** (Psychology).


2. **Technical Design Document (TDD) created and finalized:**
* This was the heavy lifting of the day. I chose a **Synchronous Monolithic Architecture** using Django.
* **Crucial Decision:** To avoid HTTP timeouts (since ML and OpenAI calls are slow), I designed a **"Store-First, Analyze-Later"** pattern.
* Endpoint A (`/sync`): Fetches data and saves to DB (Fast).
* Endpoint B (`/report`): Reads local DB and runs K-Means (Safe).




3. **Visualizing the Architecture (Mermaid.js):**
* Created the Sequence Diagrams to map the split data flow.
* Designed the Entity-Relationship Diagram (ERD), adding a `UserInsight` table to cache the expensive LLM responses.
* *Lesson Learned:* Mermaid diagrams render differently on GitHub vs. local editors. I decided to export high-res PNGs for the README and docs to ensure consistency.


4. **README Overhaul:**
* Updated the public documentation to reflect the technical reality.
* Added the new architecture diagrams and clarified the roadmap phases (Offline vs. Live).



### Technical Takeaway

It's tempting to jump straight into coding `views.py`, and continue coding indefinely, but the complexity of the project and all it's layers make difficult to have a clear view of what things needs to be done and when (earlier or after another features). Writing the **TDD** first saved me from a future headache. I almost designed a single blocking endpoint that would have definitely crashed the browser on slow networks. Splitting the logic into **ETL** vs **Inference** phases at the design stage was a win. From now on I have these documents as a quick reference that allows a clearer view of what needs to be built.

## [2026-01-05] - Project Planning & Requirements Definition

**Focus**: Researching best practices for project documentation and drafting the Product Requirements Document (PRD).

### Progress:

* **Documentation Research**: Conducted an analysis of industry-standard planning documents to ensure a structured development lifecycle.
* **Drafted the initial (PRD)**. This included:
* Defining the core problem and solution.
* Establishing the MVP scope to prevent scope creep.
* Outlining user stories and acceptance criteria.



**Goal**: To establish a clear roadmap and functional specifications before the engineering phase begins.

## [2026-01-03] - Clustering Model Finalization & Archetype definition

**Focus**: Clustering Model Finalization & Archetype definition

### Progress:

* **Model Selection**: Finalized the K-Means training and analysis. Evaluated performance using **Silhouette Score** and **Davies-Bouldin Index**, determining that 5 clusters offered better separation and psychological interpretability than 4 or 6.
* **Feature Interpretation**: Used **PCA (Principal Component Analysis)** to visualize high-dimensional data in 2D. Identified PC1 as the "Intensity Spectrum" (Organic vs. Synthetic) and PC2 as the "Mood Spectrum" (Introspective vs. Social).
* **Profile Definition**: Mapped the 5 clusters to specific backend archetypes: *The Organic/Relaxed*, *The Euphoric/Social*, *The High Intensity*, *The Rhythmic Flow*, and *The Mainstream Groove*.
* **Code Refactoring**: Split the monolithic EDA notebook into `2.0-eda-mood-distribution` and `3.0-model-clustering-profiles`.

## [2026-01-02] - Unsupervised Learning setup & Architecture research

**Focus**: Unsupervised Learning setup & Architecture research

### Progress:

* **Architecture Research**: Investigated **Decoupled Client-Server Architecture** patterns. Confirmed the strategy to use Django as a pure REST API provider serving JSON and React as a standalone consumer, ensuring separation of concerns between Data Science logic and UI.
* **EDA Pivot**: Shifted focus from descriptive statistics to **Unsupervised Machine Learning**. Prepared the dataset for clustering by removing noise and applying `StandardScaler` to normalize audio features (loudness, tempo, energy).
* **K-Means Initialization**: Implemented the **Elbow Method** to determine the optimal number of clusters. Analyzed inertia plots to identify potential inflection points between 4 and 6 clusters.

## [2026-01-01] - Variance analysis & Backend rule definition

**Focus**: Variance analysis & Backend rule definition

### Progress:

* **Distribution Profiling**: Transitioned from centroid analysis to **Boxplot Distribution** analysis. Examined the variance of Valence, Energy, and Tempo across genres.
* **Key Architectural Insight**: Discovered that mainstream genres (Pop, Latin) have high variance in emotional features, making them poor predictors of mood. Conversely, genres like EDM and Rock showed high rigidity in intensity.
* **Backend Specification**: Defined the logic for the **Psychological Profile Engine**:
* Mood: Must be calculated at the **Track-Level** (atomic).
* Intensity: Can use Genre-Level heuristics (e.g., EDM implies High Energy).


## [2025-12-30]

**Focus:** Psychometric validation & Dimensional reduction

### Progress:

* **Statistical Sanity Check**: Computed correlation matrices to identify multicollinearity. Confirmed that Valence and Energy are orthogonal (independent) dimensions in this dataset, validating their use as separate axes.
* **Affective Mapping**: Implemented Russell’s Circumplex Model, plotting 30k tracks on the Valence-Energy plane to visualize emotional quadrants.
* **Genre Clustering (Attempt 1)**: Visualized genre centroids to test if genre labels could predict emotional states. (Preliminary results suggest significant overlap).

## [2025-12-29] - Data Acquisition Strategy & Initial EDA Pipeline

**Focus:** Data Acquisition Strategy & Initial EDA Pipeline

### Progress:

* Data Source: Acquired a comprehensive dataset of ~30,000 Spotify tracks to serve as a local development proxy.
* Data Cleaning: Implemented cleaning logic using Pandas, specifically addressing duplicates and null values to ensure data integrity.
* EDA: Started Exploratory Data Analysis to understand feature distributions (valence, energy, etc.) before modeling.

### Challenges & Solutions:

* **Challenge:** Encountered authentication blockers with the Spotify for Developers API, which halted the backend integration.
* **Solution (Pivot):** Adopted a "Local Simulation" strategy. Instead of waiting on the API, I decided to use a static dataset to mock API responses. This allows the Data Science work to proceed in parallel while the authentication issues are resolved.

## [2025-12-26] - Day 1: Walking Skeleton

**Focus:** Backend and Frontend environment installation (Issue #2).

### Progress

* Successfully initialized the Django project using `uv`.
* Created the React frontend using Vite.
* **Milestone Reached:** Both servers (Django at port 8000 and React at port 5173) are running simultaneously. The "Walking Skeleton" is done!

### Challenges & Solutions

* **Node.js Version Conflict:**
* **The Problem:** While setting up the frontend, `npm run dev` failed. The default Linux repository provided Node v18.19.1, but the latest version of Vite requires Node v20+ or v22+.
* **The Fix:** Instead of relying on the system's `apt` package manager, I installed **NVM (Node Version Manager)** so I can install Node v22 cleanly without sudo permissions.
* **Lesson:** Always check engine requirements for modern frontend tools; system defaults may be outdated.

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

* Repository initialized and connected to GitHub.
* `.gitignore` file configured to avoid uploading sensitive files (`.env`) or heavy dependencies (`node_modules`, `venv`).

### Next Steps

* Initialize the Django and React (Vite) projects.
* Successfully run both servers simultaneously on my local machine.
