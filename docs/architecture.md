# Architecture

```mermaid
flowchart TD
    A[Synthetic Data Generators] --> B[Raw CSVs]
    B --> C[Python Ingestion & Cleaning]
    C --> D[(SQLite: mobility.db)]
    D --> E[dbt: Star Schema + Enriched Models]
    E --> F[Power BI Dashboard]
    E --> G[GeoPandas / Folium Geospatial Analysis]
    E --> H[scikit-learn ML Models]
    E --> I[Gemini RAG: Natural Language Q&A]
    E --> J[dbt Tests: Data Quality Gates]
    J --> K[GitHub Actions: Daily Automated Pipeline]
    K --> L[Docker: Portable Deployment]
```

## Layer descriptions

- **Ingestion:** Python scripts generate/clean raw trip and traffic data, loading it into SQLite.
- **Modeling:** dbt builds a star schema (4 dimensions, 2 facts) and two enriched, analysis-ready views, with automated tests.
- **Consumption:** the enriched models feed four independent consumers — Power BI, geospatial scripts, ML models, and the RAG system — each reading the same trusted source of truth.
- **Operations:** GitHub Actions runs the entire pipeline and test suite daily; Docker packages everything for portable, reproducible execution anywhere.