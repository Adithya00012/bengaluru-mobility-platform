import pandas as pd
import sqlite3

df = pd.read_csv("data/processed/cleaned_trips.csv")

df["speed_kmh"] = df["distance_km"] / (df["duration_min"] / 60)
df["pickup_time"] = pd.to_datetime(df["pickup_time"])
df["pickup_hour"] = df["pickup_time"].dt.hour

conn = sqlite3.connect("data/processed/mobility.db")

df.to_sql("fact_trips", conn, if_exists="replace", index=False)

result = conn.execute("SELECT COUNT(*) FROM fact_trips").fetchone()
print(f"Rows loaded into fact_trips: {result[0]}")

conn.close()
print("Saved database to data/processed/mobility.db")
