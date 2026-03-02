# ADR 005: Intelligence Engine - Google Gemini

**Date:** 2026-03-02  
**Status:** Accepted

## Context
The core value of the app is providing "psychological insights" based on music data. This requires a Large Language Model (LLM) to interpret audio features and user archetypes into human-readable personality analysis.

## Decision
We will use **Google Gemini** (via Vertex AI or Google AI SDK) as our primary intelligence engine.

## Alternatives Considered
*   **OpenAI (GPT-4o/o1):** The industry leader, but often more expensive and with stricter rate limits for free/low-tier accounts.
*   **Llama 3 (Self-hosted):** Requires significant infrastructure (GPUs) and maintenance, which is not feasible for this stage.

## Justification vs OpenAI
1.  **Python Ecosystem Integration:** Google's Python SDKs are exceptionally well-integrated with data science tools, making it easy to pass structured data from Pandas/Django to the model.
2.  **Context Window:** Gemini offers a massive context window (up to 2M tokens), which is beneficial if we ever need to feed it large amounts of historical listening data or entire datasets for analysis.
3.  **Multimodal Capabilities:** Gemini's native multimodality could allow future features like analyzing album art or music videos alongside audio features.
4.  **Cost Efficiency:** For many use cases, Gemini (especially Pro and Flash models) offers a more competitive price-to-performance ratio than OpenAI's flagship models.
5.  **Free Tier:** Google provides a generous free tier for developers, which is ideal for the "Simulation Mode" and early development phases.

## Consequences
*   **Positive:** Lower costs during development, easy integration with Python, and future-proof context window.
*   **Negative:** Slightly different prompting techniques compared to OpenAI's models.
