# ADR 004: Deployment Platform - Railway

**Date:** 2026-03-02  
**Status:** Accepted

## Context
We need a cloud platform to host our full-stack application, including the Django backend, PostgreSQL database, and Next.js frontend.

## Decision
We will use **Railway** as our primary deployment and infrastructure platform.

## Alternatives Considered
*   **Vercel:** Excellent for Next.js but difficult for hosting persistent Django backends and full PostgreSQL databases.
*   **Heroku:** Historically the standard, but now more expensive and with a less modern developer experience.
*   **AWS/GCP:** Too complex for the current stage of the project, requiring significant DevOps overhead.

## Justification
1.  **Unified Environment:** Railway allows us to host the backend, frontend, and database in a single "Project," sharing environment variables easily.
2.  **Native Django Support:** Unlike Vercel, Railway runs Django as a persistent service, which is how the framework is designed to operate.
3.  **One-Click PostgreSQL:** Provisioning a production-ready database is instantaneous.
4.  **Cost-Effective:** The "pay-as-you-go" model is ideal for a growing project, often being cheaper than competitors for similar resources.

## Consequences
*   **Positive:** Simplified DevOps, fast deployments, and all infrastructure in one place.
*   **Negative:** We lose some of the "Edge" optimizations specific to Vercel for the Next.js frontend, though the impact is negligible for this use case.
