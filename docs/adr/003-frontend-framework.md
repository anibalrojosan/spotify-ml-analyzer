# ADR 003: Frontend Framework - Next.js

**Date:** 2026-03-02  
**Status:** Accepted

## Context
The application needs a modern, interactive user interface to display complex data visualizations (radar charts, scatter plots) and handle user authentication flows.

## Decision
We will use **Next.js** (App Router) as the frontend framework.

## Alternatives Considered
*   **Vite + React (SPA):** Simpler for very small projects, but lacks built-in routing, SEO optimizations, and server-side capabilities.
*   **Remix:** A strong competitor, but Next.js has a larger ecosystem and better integration with deployment platforms like Vercel and Railway.

## Justification
1.  **App Router:** Provides a modern way to handle routing and layouts, improving developer experience.
2.  **Server-Side Rendering (SSR):** Allows for faster initial page loads and better handling of sensitive data (like API keys) on the server side.
3.  **Ecosystem:** Excellent support for visualization libraries like **Recharts** or **D3.js**, which are critical for our data-driven dashboard.
4.  **Scalability:** Next.js is designed to scale from a small prototype to a large production application.

## Consequences
*   **Positive:** High performance, great developer experience, and easy deployment.
*   **Negative:** More complex than a basic React SPA.
