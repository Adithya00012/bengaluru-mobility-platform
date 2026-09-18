import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

df = pd.read_sql("SELECT * FROM fact_trips", conn)

conn.close()

df.to_csv("data/processed/trips_for_powerbi.csv", index=False)

print(f"Exported {len(df)} rows to data/processed/trips_for_powerbi.csv")
