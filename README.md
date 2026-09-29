# Bengaluru Mobility Intelligence Platform

An end-to-end urban mobility analytics platform for Bengaluru, covering data ingestion, dimensional modeling, transformation, geospatial analysis, machine learning, natural language querying, cloud data warehousing, and automated deployment.

## Architecture
```text
Synthetic/Raw Data → Python Ingestion → SQLite → dbt (star schema) →
├── Power BI Dashboard (3 pages: Trips, Congestion, Predictions & Routes)
├── GeoPandas/Folium Geospatial Analysis
├── scikit-learn ML Models (travel-time prediction, congestion classification, anomaly detection)
├── Gemini-powered Natural Language Q&A (RAG)
├── Google BigQuery (cloud data warehouse, synced daily)
└── Excel export (stakeholder-friendly scenario analysis)
```
Entire pipeline automated via GitHub Actions (daily + weekly), containerized with Docker (full parity with CI, including dbt).


See `docs/architecture.md` for a full diagram and `docs/schema.md` for the entity-relationship model.

## What's built

**Data Engineering:** Star schema — `dim_date` (with real 2026 Karnataka holidays), `dim_time`, `dim_location`, `dim_weather`, `dim_events`, `fact_trips` (with pickup **and** dropoff zones), `fact_traffic` — managed with dbt (models, automated tests, auto-generated documentation). Cleaning handles invalid durations, missing data, duplicate records, and missing coordinates.

**Analytics & Geospatial:** Interactive zone-demand mapping, real inter-zone distance calculations (Haversine + UTM projection), congestion ranking, route-level (origin-destination) delay analysis, weather and holiday impact analysis, event-impact analysis, threshold-based congestion alerts, and time-window/route recommendations.

**Machine Learning:** Linear regression for travel-time prediction (R² 0.82 on 480 synthetic trips), decision tree classification for congestion prediction (86% accuracy, 9.3pp above baseline on 3,840 synthetic traffic readings), and z-score based anomaly detection for trip volume and congestion spikes. See `docs/ml_experiment_notes.md` for the full experimental history.

**Natural Language Intelligence (RAG):** A text-to-SQL pipeline using Google's Gemini API — see `docs/api_documentation.md` for integration details.

**Automation & Monitoring:** GitHub Actions runs the full pipeline daily (and a weekly-labeled report every Monday), including dbt tests, automated report generation (Markdown + Excel), and a daily sync to BigQuery — all authenticated via a scoped service account stored in GitHub Secrets, with automatic failure notifications.

**Cloud Data Warehouse:** The full star schema is deployed to Google BigQuery (free sandbox tier), kept in sync automatically by the daily pipeline. A second, isolated dbt project (`bengaluru_mobility_dbt_bigquery/`) runs the same enrichment model directly against BigQuery.

**Deployment:** Fully containerized with Docker — the container runs the complete pipeline including dbt build and test, matching what GitHub Actions runs.

## Project structure
```text
bengaluru-mobility-platform/
├── data/
│ ├── raw/ # Source CSVs + synthetic data generators' output
│ └── processed/ # Cleaned data, SQLite database, Power BI exports
├── src/
│ ├── ingestion/ # Loading, cleaning, dimension/fact table builders
│ ├── analysis/ # Geospatial, congestion, route, event, recommendation scripts
│ ├── ml/ # ML models + anomaly detection
│ ├── rag/ # Natural language Q&A (Gemini)
│ ├── run_pipeline.py # Orchestrates the Python ingestion pipeline
│ ├── generate_report.py # Daily/weekly Markdown report generator
│ ├── export_to_excel.py # Stakeholder-friendly Excel export
│ └── load_to_bigquery.py # Syncs the star schema to BigQuery
├── bengaluru_mobility_dbt/ # dbt project (SQLite target)
├── bengaluru_mobility_dbt_bigquery/ # dbt project (BigQuery target)
├── dashboards/ # Power BI dashboard, exported geospatial maps
├── docs/ # Data dictionary, schema, architecture, troubleshooting, API docs, ML notes
├── reports/ # Generated Markdown + Excel reports
├── .github/workflows/ # GitHub Actions automation
├── Dockerfile
└── requirements.txt
```

## Running this project

**Locally:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/run_pipeline.py
cd bengaluru_mobility_dbt && dbt run && dbt test
```

**With Docker** (runs the full pipeline including dbt):
```bash
docker build -t bengaluru-mobility-platform .
docker run --rm bengaluru-mobility-platform
```

**Natural language queries** (requires a free Gemini API key in `.env` — see `docs/api_documentation.md`):
```bash
python3 src/rag/ask_mobility_data.py
```

**BigQuery sync** (requires `gcloud auth application-default login` locally, or `GCP_SA_KEY` in CI):
```bash
python3 src/load_to_bigquery.py
```

## Documentation

- `docs/data_dictionary.md` — column-level detail for every table
- `docs/schema.md` — entity-relationship diagram
- `docs/architecture.md` — system architecture diagram
- `docs/api_documentation.md` — Gemini API integration details
- `docs/troubleshooting.md` — real issues encountered and their fixes
- `docs/ml_experiment_notes.md` — full ML experimentation history

## A note on data volume and model performance

The project started with a small, hand-crafted sample dataset (30 trips, 10 traffic readings). At that scale, the ML models performed poorly (negative R², near-baseline classification accuracy) — a genuine, correctly-diagnosed data volume limitation. The dataset was expanded using realistic synthetic data generators (480 trips, 3,840 traffic readings across 30 days, with real peak-hour and zone-level patterns built in). With the same modeling code, R² improved to 0.82 and classification accuracy to 86% — evidence the methodology was sound throughout; the models only needed real data volume.

## Tech stack

Python (pandas, GeoPandas, Folium, scikit-learn, google-genai, google-cloud-bigquery), SQL, SQLite, BigQuery, dbt, Power BI, Excel, Docker, GitHub Actions, Git.