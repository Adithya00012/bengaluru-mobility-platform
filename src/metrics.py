import pandas as pd

df = pd.read_csv("data/processed/cleaned_trips.csv")

df["pickup_time"] = pd.to_datetime(df["pickup_time"])
df["dropoff_time"] = pd.to_datetime(df["dropoff_time"])

avg_duration = df["duration_min"].mean()

df["speed_kmh"] = df["distance_km"] / (df["duration_min"] / 60)
avg_speed = df["speed_kmh"].mean()

raw_df = pd.read_csv("data/raw/sample_trips.csv")
total_raw = len(raw_df)
total_clean = len(df)
completion_rate = (total_clean / total_raw) * 100

df["pickup_hour"] = df["pickup_time"].dt.hour
demand_by_hour = df.groupby("pickup_hour")["trip_id"].count()

print("=== Bengaluru Mobility Metrics (Sample Data) ===\n")
print(f"Average travel time: {avg_duration:.1f} minutes")
print(f"Average speed: {avg_speed:.1f} km/h")
print(
    f"Trip completion rate: {completion_rate:.1f}% ({total_clean} of {total_raw} trips)"
)
print("\nDemand by pickup hour:")
print(demand_by_hour)

import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

speed_stats = pd.read_sql(
    "SELECT AVG(speed_kmh) as avg_speed FROM fact_trips_enriched", conn
).iloc[0]["avg_speed"]
delay_threshold = speed_stats * 0.7

delay_query = f"""
SELECT
    COUNT(*) as total_trips,
    SUM(CASE WHEN speed_kmh < {delay_threshold} THEN 1 ELSE 0 END) as delayed_trips
FROM fact_trips_enriched
"""
delay_stats = pd.read_sql(delay_query, conn)
conn.close()

delay_percentage = (
    delay_stats.iloc[0]["delayed_trips"] / delay_stats.iloc[0]["total_trips"]
) * 100

print(f"\n=== Delay Percentage (current dataset) ===")
print(f"Network average speed: {speed_stats:.1f} km/h")
print(f"Delay threshold (30% below average): {delay_threshold:.1f} km/h")
print(
    f"Delayed trips: {delay_stats.iloc[0]['delayed_trips']} of {delay_stats.iloc[0]['total_trips']}"
)
print(f"Delay percentage: {delay_percentage:.1f}%")
