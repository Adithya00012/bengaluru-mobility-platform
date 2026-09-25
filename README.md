# Bengaluru Mobility Intelligence Platform

An end-to-end urban mobility analytics platform for Bengaluru, built to demonstrate the full data lifecycle: ingestion, dimensional modeling, transformation, geospatial analysis, machine learning, natural language querying, and automated deployment.

## Architecture
Synthetic/Raw Data → Python Ingestion → SQLite → dbt (star schema) →
├── Power BI Dashboard
├── GeoPandas/Folium Geospatial Analysis
├── scikit-learn ML Models (travel-time prediction, congestion classification)
└── Gemini-powered Natural Language Q&A (RAG)

Entire pipeline automated via GitHub Actions (daily) and containerized with Docker.


## What's built

**Data Engineering:** Star schema with `dim_date`, `dim_time`, `dim_location`, `dim_weather`, `fact_trips`, `fact_traffic`, managed with dbt (models, automated tests, auto-generated documentation).

**Analytics & Geospatial:** Interactive zone-demand mapping, real inter-zone distance calculations (Haversine + UTM projection), congestion ranking, delayed-trip detection, weather impact analysis.

**Machine Learning:** Linear regression for travel-time prediction (R² 0.82 on 480 synthetic trips) and decision tree classification for congestion prediction (86% accuracy, 9.3pp above baseline on 3,840 synthetic traffic readings). See [A note on data volume](#a-note-on-data-volume-and-model-performance) below.

**Natural Language Intelligence (RAG):** A text-to-SQL pipeline using Google's Gemini API — converts plain-English questions into real SQL queries, runs them against the actual database, and returns grounded, natural-language answers.

**Automation & Monitoring:** GitHub Actions workflow runs the full pipeline and dbt tests daily, with automatic failure notifications and a run summary.

**Deployment:** Fully containerized with Docker for portable, reproducible execution.

## Project structure

bengaluru-mobility-platform/
├── data/
│ ├── raw/ # Source CSVs (including synthetic data generators' output)
│ └── processed/ # Cleaned data, SQLite database
├── src/
│ ├── ingestion/ # Data loading, cleaning, dimension/fact table builders
│ ├── analysis/ # Geospatial and congestion analysis scripts
│ ├── ml/ # Machine learning models
│ ├── rag/ # Natural language Q&A (Gemini)
│ └── run_pipeline.py # Orchestrates the full pipeline
├── bengaluru_mobility_dbt/ # dbt project (models, tests, docs)
├── dashboards/ # Power BI dashboard, exported geospatial maps
├── .github/workflows/ # GitHub Actions automation
├── Dockerfile
└── requirements.txt


## Running this project

**Locally:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/run_pipeline.py
cd bengaluru_mobility_dbt && dbt run && dbt test
```

**With Docker:**
```bash
docker build -t bengaluru-mobility-platform .
docker run --rm bengaluru-mobility-platform
```

**Natural language queries** (requires a free Gemini API key in a `.env` file — see `GEMINI_API_KEY` in `src/rag/ask_mobility_data.py`):
```bash
python3 src/rag/ask_mobility_data.py
```

## A note on data volume and model performance

The project started with a small, hand-crafted sample dataset (30 trips, 10 traffic readings) to make every pipeline step fast to run and inspect. At that scale, the Phase 4 ML models performed poorly (negative R² for travel-time regression, near-baseline accuracy for congestion classification) — a genuine, correctly-diagnosed data volume limitation, not a flaw in the modeling approach.

The dataset was then expanded using a realistic synthetic data generator (`src/ingestion/generate_synthetic_trips.py`, `generate_synthetic_traffic.py`) — 480 trips and 3,840 traffic readings across 30 days, with genuine peak-hour and zone-level patterns built in. With this larger dataset, using the exact same pipeline and modeling code:

- **Travel-time regression:** R² improved from -0.72 to **0.82**, with mean absolute error down to 5.8 minutes.
- **Congestion classification:** accuracy improved from 33% (worse than baseline) to **86%**, a 9.3 percentage-point improvement over the majority-class baseline.

This progression is intentionally documented as evidence the underlying methodology was sound throughout — the models only needed real data volume, not different code.

## Tech stack

Python (pandas, GeoPandas, Folium, scikit-learn, google-genai), SQL, SQLite, dbt, Power BI, Docker, GitHub Actions, Git.