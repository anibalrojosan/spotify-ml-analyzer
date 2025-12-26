# 📝 Development Log

This document serves as a chronological record of the **Spotify ML Analyzer** development. Here, I document technical decisions, challenges faced, solutions, and lessons learned.

The goal is to maintain transparency throughout the process and generate a clear history of my "train of thought."

---

## [2025-12-26] - Day 0

**Status:** 🟡 In Progress

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