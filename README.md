# Bengaluru Mobility Intelligence Platform

A portfolio data engineering and analytics project simulating an urban mobility platform for Bengaluru — covering data ingestion, a dimensional data model, dbt transformations, geospatial analysis, and machine learning.

## What's built so far

**Phase 1 — MVP:** Python ingestion, data cleaning, SQLite storage, core mobility metrics, and a Power BI dashboard, fully automated via a single pipeline script.

**Phase 2 — Data Engineering:** A full star schema (`dim_date`, `dim_time`, `dim_location`, `dim_weather`, `fact_trips`, `fact_traffic`), managed with dbt — including automated data tests and auto-generated documentation.

**Phase 3 — Advanced Analytics & Geospatial:** Interactive zone-demand mapping (GeoPandas + Folium), real inter-zone distance calculations, congestion ranking, delayed-trip detection, and weather impact analysis.

**Phase 4 — Machine Learning (in progress):** Travel-time prediction (linear regression) and congestion classification (decision tree).

## A note on data volume and model performance

The project started with a small, hand-crafted sample dataset (30 trips, 10 traffic readings) to make every pipeline step fast to run and inspect. At that scale, the Phase 4 ML models performed poorly (negative R² for travel-time regression, near-baseline accuracy for congestion classification) — a genuine, correctly-diagnosed data volume limitation, not a flaw in the modeling approach.

The dataset was then expanded using a realistic synthetic data generator (`src/ingestion/generate_synthetic_trips.py`, `generate_synthetic_traffic.py`) — 480 trips and 3,840 traffic readings across 30 days, with genuine peak-hour and zone-level patterns built in. With this larger dataset, using the exact same pipeline and modeling code:

- **Travel-time regression:** R² improved from -0.72 to **0.82**, with mean absolute error down to 5.8 minutes. The model correctly identified that peak-hour trips take ~18 minutes longer, matching the pattern built into the simulation.
- **Congestion classification:** accuracy improved from 33% (worse than baseline) to **86%**, a 9.3 percentage-point improvement over the majority-class baseline, after also increasing model complexity (tree depth) to match the larger data volume.

This progression — correctly diagnosing weak performance as a data problem, then validating the same pipeline against a larger dataset — is intentionally documented here as evidence the underlying methodology was sound throughout.

## Tech stack

Python (pandas, GeoPandas, Folium, scikit-learn), SQL, SQLite, dbt, Power BI, Git/GitHub.