# Database Schema - Spotify ML Analyzer

This document details the PostgreSQL database schema implemented for **Phase 2: Simulation Engine**.

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    TRACK ||--|| AUDIO_FEATURES : "has"
    USER_PROFILE }|--|| USER_ARCHETYPE : "assigned_to"
    USER_PROFILE }o--o{ TRACK : "listens_to"
    USER_PROFILE ||--o{ USER_INSIGHT : "receives"

    TRACK {
        uuid id PK "Internal UUID"
        varchar spotify_id UK "Spotify URI (Indexed)"
        varchar title
        varchar artist_name
        varchar album_name
        timestamp created_at
        timestamp updated_at
    }

    AUDIO_FEATURES {
        int id PK
        uuid track_id FK "Unique Link to Track"
        float danceability "0.0 - 1.0"
        float energy "0.0 - 1.0"
        float valence "0.0 - 1.0 (Positivity)"
        float acousticness "0.0 - 1.0"
        float tempo "BPM"
        float instrumentalness "0.0 - 1.0"
        float liveness "0.0 - 1.0"
        float loudness "dB"
        float speechiness "0.0 - 1.0"
    }

    USER_ARCHETYPE {
        int id PK
        varchar name UK "Slug (e.g. sad-rocker)"
        varchar display_name
        text description
        jsonb min_values "Range definition"
        jsonb max_values "Range definition"
    }

    USER_PROFILE {
        int id PK
        varchar spotify_id UK "Real or Mock ID"
        varchar display_name
        int archetype_id FK "Nullable"
        timestamp created_at
        timestamp updated_at
    }

    USER_INSIGHT {
        int id PK
        int user_id FK
        varchar personality_label
        text llm_response "Gemini Output"
        jsonb cluster_centers "Chart Data"
        timestamp created_at
    }
```

## Data Dictionary

### Table: `api_track`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID | PK, Default `uuid4` | Internal unique system identifier. |
| `spotify_id` | VARCHAR(255) | Unique, Indexed | Original Spotify ID (e.g., `4iV5W9u...`). Business key. |
| `title` | VARCHAR(255) | Not Null | Song title. |
| `artist_name` | VARCHAR(255) | Not Null | Main artist name. |
| `album_name` | VARCHAR(255) | Not Null | Album name. |

### Table: `api_audiofeatures`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `track_id` | UUID | FK (Track), Unique | 1:1 relationship with the Tracks table. |
| `danceability` | FLOAT | Not Null | How suitable a track is for dancing (0.0 to 1.0). |
| `energy` | FLOAT | Not Null | Perceptual measure of intensity and activity (0.0 to 1.0). |
| `valence` | FLOAT | Not Null | Musical positiveness (0.0 = sad, 1.0 = happy). |
| `tempo` | FLOAT | Not Null | Estimated tempo in BPM. |
| `loudness` | FLOAT | Default 0.0 | Average loudness in decibels (dB). |

### Table: `api_userarchetype`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `name` | VARCHAR(50) | Unique, Slug | Technical identifier (e.g., `high-intensity`). |
| `min_values` | JSONB | Not Null | Dictionary with minimum values to filter tracks for this archetype. |
| `max_values` | JSONB | Not Null | Dictionary with maximum values. |

### Table: `api_userprofile`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `spotify_id` | VARCHAR(255) | Unique | User ID (simulated or real). |
| `archetype_id` | INT | FK (UserArchetype), Nullable | Archetype assigned to the current session. |
| `tracks` | M2M | - | Many-to-Many relationship with `Track` (Listening history). |
