# Bengaluru Mobility Intelligence Platform

A portfolio data engineering and analytics project simulating an urban mobility platform for Bengaluru — covering data ingestion, a dimensional data model, dbt transformations, geospatial analysis, and machine learning.

## What's built so far

**Phase 1 — MVP:** Python ingestion, data cleaning, SQLite storage, core mobility metrics, and a Power BI dashboard, fully automated via a single pipeline script.

**Phase 2 — Data Engineering:** A full star schema (`dim_date`, `dim_time`, `dim_location`, `dim_weather`, `fact_trips`, `fact_traffic`), managed with dbt — including automated data tests and auto-generated documentation.

**Phase 3 — Advanced Analytics & Geospatial:** Interactive zone-demand mapping (GeoPandas + Folium), real inter-zone distance calculations, congestion ranking, delayed-trip detection, and weather impact analysis.

**Phase 4 — Machine Learning (in progress):** Travel-time prediction (linear regression) and congestion classification (decision tree).

## A note on data volume and model performance

This project uses a small, hand-crafted sample dataset (30 trips, 10 traffic readings) so that every step of the pipeline — ingestion, cleaning, modeling, testing, ML — can be run, inspected, and understood quickly.

This has an honest consequence for the Phase 4 ML models: with so few data points, both the travel-time regression and congestion classification models show weak, sometimes worse-than-baseline performance (negative R², low classification accuracy). This isn't a flaw in the modeling approach — it's an expected and correctly-diagnosed limitation of the data volume. The pipelines (feature engineering, train/test splitting, avoiding data leakage, honest evaluation) are built correctly and would perform meaningfully better on a real, larger dataset without needing to change the underlying code.

## Tech stack

Python (pandas, GeoPandas, Folium, scikit-learn), SQL, SQLite, dbt, Power BI, Git/GitHub.