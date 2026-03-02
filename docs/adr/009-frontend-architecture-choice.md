# ADR 009: Frontend Architecture - Next.js over Streamlit

**Date:** 2026-03-02  
**Status:** Accepted

## Context
The project requires a frontend to visualize music data, user archetypes, and AI-generated insights. We need to decide between a rapid prototyping tool like **Streamlit** and a full-stack framework like **Next.js** with component libraries.

## Decision
We will use **Next.js** (App Router) combined with **Tailwind CSS** and **Shadcn/UI** (component library) instead of Streamlit.

## Alternatives Considered
*   **Streamlit:** A Python-based framework for rapid data app prototyping.
*   **Vite + React:** A standard React SPA setup.

## Justification: Why NOT Streamlit?
1.  **Throwaway Code:** Streamlit is Python-based. Moving from a Streamlit prototype to a production-ready mobile/desktop app would require a 100% rewrite of the frontend in a different language (TypeScript/JavaScript).
2.  **Aesthetic Limitations:** Streamlit has a rigid, "data-tool" look that is difficult to customize. It cannot achieve the modern, Spotify-like aesthetic required for the final product.
3.  **UX & Performance:** Streamlit's execution model (re-running the script on every interaction) is not suitable for highly interactive dashboards with smooth transitions and complex state management.
4.  **Mobile Support:** Streamlit is not designed for "Mobile-First" or responsive design, which is a key requirement for the project's evolution.

## Justification: Why Next.js + Component Libraries?
1.  **Professional UI/UX:** Libraries like **Shadcn/UI** and **Tailwind CSS** allow for rapid building of professional, highly customizable interfaces that look like real products from day one.
2.  **Learning & Scalability:** Using Next.js provides a valuable learning opportunity for a modern, industry-standard stack that scales from a prototype to a production-grade application.
3.  **API-First Thinking:** Next.js forces the development of a clean API layer in Django, which is essential for the future Spotify API integration (Phase 5).
4.  **Evolutive Development:** The code written for the Phase 3 prototype will serve as the actual foundation for the final product, avoiding the "double work" associated with throwaway prototypes.

## Consequences
*   **Positive:** High-quality, responsive UI; reusable code; professional-grade tech stack; better preparation for live API integration.
*   **Negative:** Higher initial learning curve compared to Streamlit (requires basic knowledge of React and TypeScript).
