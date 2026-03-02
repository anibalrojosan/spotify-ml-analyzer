# ADR 001: Backend Framework - Django + Django REST Framework

**Date:** 2026-03-02  
**Status:** Accepted

## Context
The project requires a robust backend to handle complex data models (tracks, audio features, user archetypes), manage authentication (both mock and real Spotify OAuth 2.0), and expose a secure API for the frontend.

## Decision
We will use **Django** as the primary backend framework, specifically utilizing **Django REST Framework (DRF)** for API development.

## Alternatives Considered
*   **Flask:** Popular for small to medium-sized projects, but lacks the features and community support of Django.
*   **FastAPI:** Known for high performance and modern Python features (async). However, it requires more manual configuration for authentication and database management.
*   **Node.js (Express/NestJS):** Popular for real-time apps, but less integrated with the Python data science ecosystem (Pandas, Scikit-learn) which is central to the project.

## Justification
1.  **Powerful ORM:** Django's ORM is ideal for managing the relational data of tracks and users, making migrations and database schema management seamless.
2.  **Built-in Security:** Django provides robust protection against common vulnerabilities (CSRF, XSS, SQL Injection) out of the box.
3.  **Authentication Ecosystem:** Libraries like `django-allauth` and `social-auth-app-django` simplify the integration with Spotify OAuth 2.0.
4.  **Admin Interface:** The built-in admin panel allows for quick data inspection and management during development.

## Consequences
*   **Positive:** Faster development of the data layer and authentication. High maintainability.
*   **Negative:** Steeper learning curve compared to micro-frameworks like Flask. Slightly higher memory overhead.
