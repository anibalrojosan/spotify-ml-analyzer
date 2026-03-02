# ADR 002: Persistence Strategy - PostgreSQL

**Date:** 2026-03-02  
**Status:** Accepted

## Context
Currently, the project uses static CSV files for data storage during the "Simulation Mode". We need a long-term persistence strategy that supports both the simulation and the future "Live Mode" with Spotify API integration.

## Decision
We will use **PostgreSQL** as our primary relational database from the start of Phase 2.

## Alternatives Considered
*   **In-Memory CSV (Pandas):** Simple for prototyping but doesn't scale and requires a massive refactor when moving to live data.
*   **SQLite:** Good for local development, but lacks some advanced features and isn't ideal for production environments like Railway.
*   **NoSQL (MongoDB):** Not suitable for our highly structured and relational music data.

## Justification
1.  **Seamless Transition:** By using PostgreSQL in Phase 2, we can ingest CSV data into real tables. When we switch to the Spotify API (Phase 5), the backend and frontend logic won't need to change—only the data source.
2.  **Django Integration:** Django's ORM is optimized for PostgreSQL, supporting advanced features like JSONB and full-text search if needed.
3.  **Data Integrity:** Relational constraints ensure that track features, user profiles, and archetypes remain consistent.
4.  **Production Ready:** PostgreSQL is the industry standard for reliable, scalable data storage.

## Consequences
*   **Positive:** No "re-work" required when switching to live data. Robust data management.
*   **Negative:** Requires setting up a database server (handled by Railway) and managing migrations.
