import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")
df = pd.read_sql("SELECT * FROM fact_traffic_enriched", conn)
conn.close()

df.to_csv("data/processed/traffic_for_powerbi.csv", index=False)
print(f"Exported {len(df)} rows to data/processed/traffic_for_powerbi.csv")
