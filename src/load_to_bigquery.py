import pandas as pd
import sqlite3
from google.cloud import bigquery

PROJECT_ID = "bengaluru-mobility-platform"
DATASET_ID = "mobility_data"

client = bigquery.Client(project=PROJECT_ID)
conn = sqlite3.connect("data/processed/mobility.db")

tables = ["dim_date", "dim_time", "dim_location", "dim_weather", "dim_events", "fact_trips", "fact_traffic"]

for table_name in tables:
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  

    print(f"Loaded {len(df)} rows into {table_id}")

conn.close()
print("\nAll tables migrated to BigQuery successfully")