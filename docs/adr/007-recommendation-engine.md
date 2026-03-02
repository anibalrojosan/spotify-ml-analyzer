# ADR 007: Recommendation Engine Implementation - Scikit-learn Serialization

**Date:** 2026-03-02  
**Status:** Accepted

## Context
The application provides music recommendations based on user archetypes and audio features. We need a way to move the machine learning models from the research phase (Notebooks) to the production environment (Django API).

## Decision
We will use **Scikit-learn** for the recommendation logic (KNN) and **Joblib/Pickle** for model serialization.

## Alternatives Considered
*   **Vector Database (e.g., Pinecone, pgvector):** Powerful for massive datasets, but adds unnecessary complexity and cost for our current scale (~thousands of tracks).
*   **Pure SQL Similarity:** Possible but lacks the flexibility and advanced distance metrics provided by specialized ML libraries.

## Justification
1.  **Seamless Transition:** Allows us to directly use the models developed and validated in the Jupyter Notebooks.
2.  **Performance:** Loading a pre-trained KNN model into memory at Django startup is extremely fast for the current dataset size.
3.  **Simplicity:** Minimal infrastructure overhead. No need for external vector search services.
4.  **Consistency:** Ensures that the recommendations in the app match the results found during the EDA and research phase.

## Consequences
*   **Positive:** Fast implementation and high accuracy based on research.
*   **Negative:** The model needs to be re-serialized and re-loaded if the underlying training data changes significantly.
