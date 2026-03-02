# ADR 008: Frontend State & Visualization - Zustand + Recharts

**Date:** 2026-03-02  
**Status:** Accepted

## Context
The frontend needs to manage complex state (current user archetype, track lists, audio feature comparisons) and render interactive data visualizations (Radar Charts, Scatter Plots).

## Decision
We will use **Zustand** for state management and **Recharts** for data visualization.

## Alternatives Considered
*   **Redux Toolkit:** Powerful but overly verbose and complex for a project of this scale.
*   **React Context API:** Simple but can lead to performance issues (unnecessary re-renders) in complex data-driven dashboards.
*   **D3.js:** Extremely powerful but has a very steep learning curve and is harder to integrate with React's declarative style compared to Recharts.

## Justification
1.  **Zustand:** Offers a minimal, fast, and scalable state management solution with almost zero boilerplate. Perfect for handling the "Mock User" and "Live User" sessions.
2.  **Recharts:** Built specifically for React. It provides high-level components for Radar and Scatter charts that are easy to style and integrate with our data models.
3.  **Developer Velocity:** Both libraries prioritize ease of use without sacrificing performance, allowing us to build the visual prototype (Phase 3) quickly.

## Consequences
*   **Positive:** Fast development of the dashboard, clean state management, and responsive visualizations.
*   **Negative:** Recharts is less flexible than D3 for highly custom/experimental visualizations (not a concern for current requirements).
