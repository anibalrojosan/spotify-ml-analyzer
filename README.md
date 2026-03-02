# 🎵 Spotify ML Analyzer: Your Musical DNA Decoded

![Status](https://img.shields.io/badge/Status-In%20Development-yellow) ![Stack](https://img.shields.io/badge/Stack-Full%20Stack%20Data%20Science-blueviolet)

> This project is under active development. You can check the [DEVLOG](docs/development/DEVLOG.md) to follow my progress, technical hurdles, and implemented solutions while building this app.

Most apps tell you *what* you listen to. **Spotify ML Analyzer** explains **who you are** through your music.

This application acts as a "Psychological Musical Mirror." It connects to your Spotify account, extracts complex audio metrics and uses unsupervised Machine Learning to group your taste into personality profiles. Finally, an AI Agent interprets these profiles to give you a text-based 'taste' analysis.

## Index

- [🔑 Key Features](#key-features)
- [📈Project Evolution](#project-evolution)
- [📂 Project Structure](#project-structure)
- [🛠️ Tech Stack](#tech-stack)


## Key Features
* **Real Authentication:** Secure login via Spotify (OAuth 2.0).
* **Deep Analysis:** Extraction of "Audio Features" hidden from the official app.
* **ML Profiling:** Using **K-Means Clustering** to identify your distinct musical moods.
* **AI Insights:** Integration with **OpenAI** to generate personality descriptions.
* **Visualization:** Radar Charts & Scatter Plots to see your cluster distribution.

## Project Evolution

Beyond the code, this project follows rigorous engineering practices. You can read the detailed specifications here:

| Document | Description |
| :--- | :--- |
| **[PRD](./docs/PDR.md)** | Features, user stories, and MVP scope definition. |
| **[ARCHITECTURE](./docs/ARCHITECTURE.md)** | System design, "Store-First" strategy, and database schema. |
| **[ROADMAP](./docs/ROADMAP.md)** | Project evolution and roadmap. |

## Project Structure

```
spotify-analyzer/
├── backend/                  # 🐍 Django Backend
│   ├── api/                  # API endpoints
│   ├── core/                 # Django project configuration (settings, urls)
│   ├── data/                 # 📊 Datasets
│   ├── db.sqlite3            # Development database (SQLite)
│   └── manage.py
├── docs/                     # 📝 Documentation
│   ├── ARCHITECTURE.md
│   ├── PDR.md
│   ├── ROADMAP.md
│   ├── development/          # DEVLOG.md
│   └── images/               # Diagrams (ER, Architecture)
├── notebooks/                # 📓 Jupyter Notebooks (EDA, Clustering, Cleaning)
├── pyproject.toml            # Project dependencies
└── README.md                 # Project documentation
```

## Tech Stack
* **Frontend:** `Next.js` (App Router) + `TypeScript` + `Tailwind CSS` + `Shadcn/UI` + `Zustand` + `Recharts`
* **Backend:** `Python 3.12+`, `Django 5.x`, `Django REST Framework (DRF)`
* **Data Science:** `Scikit-learn`, `Pandas`, `NumPy`
* **GenAI:** `Gemini API` (Personality Insights & Roasts)
* **Database:** `PostgreSQL` (Live Mode) + `In-Memory CSV` (Simulation Mode)
* **Tooling:** `uv`, `Ruff` (Linter), `Pytest` (Testing)
* **Infrastructure:**  `Docker`, `Railway` (Deployment)

> Done with ❤️ by [Aníbal Rojo](https://github.com/anibalrojosan).