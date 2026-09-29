FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Tell dbt where the project root is, matching the profiles.yml template
ENV DBT_ROOT=/app
ENV DBT_PROFILES_DIR=/app/.dbt

# Run ingestion, then dbt build + test, in one command
CMD ["sh", "-c", "python3 src/run_pipeline.py && cd bengaluru_mobility_dbt && dbt run && dbt test"]