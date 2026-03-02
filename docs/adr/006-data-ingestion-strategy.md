# ADR 006: Data Ingestion Strategy - Unified Ingestor Pattern

**Date:** 2026-03-02  
**Status:** Accepted

## Context
The project needs to ingest music data from two different sources at different stages: static CSV files (Phase 2) and the Spotify API (Phase 5). We need a strategy that minimizes code duplication and ensures data consistency across these sources.

## Decision
We will implement a **Unified Ingestor Pattern** using **Custom Django Management Commands**.

## Alternatives Considered
*   **Ad-hoc Python Scripts:** Fast to write but difficult to integrate with the Django ORM and hard to maintain as the project grows.
*   **Direct SQL COPY:** Extremely fast for CSVs but bypasses Django's validation logic and doesn't work for API-based ingestion.

## Justification
1.  **Validation:** Using Django Management Commands allows us to use the ORM to validate data (e.g., checking for duplicates, ensuring correct types) before it hits the database.
2.  **Reusability:** We can create a base `BaseIngestor` class that handles the database logic, with specific subclasses for `CSVIngestor` and `SpotifyAPIIngestor`.
3.  **Automation:** Management commands can be easily triggered in production (Railway) via cron jobs or deployment hooks.
4.  **Consistency:** Ensures that the database schema is the "source of truth" regardless of where the data comes from.

## Consequences
*   **Positive:** Clean separation between data sources and database logic. Easy transition from Phase 2 to Phase 5.
*   **Negative:** Requires more initial setup than a simple script.
