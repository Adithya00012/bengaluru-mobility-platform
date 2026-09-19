import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

traffic = pd.read_csv("data/raw/sample_traffic.csv")
dim_location = pd.read_sql("SELECT * FROM dim_location", conn)

traffic = traffic.merge(
    dim_location[["zone_id", "zone_name"]], on="zone_name", how="left"
)

traffic["reading_time"] = pd.to_datetime(traffic["reading_time"])
traffic["date_id"] = traffic["reading_time"].dt.strftime("%Y%m%d").astype(int)
traffic["time_id"] = traffic["reading_time"].dt.hour

fact_traffic = traffic[
    ["date_id", "time_id", "zone_id", "avg_speed_kmh", "congestion_index"]
]

print("fact_traffic shape:", fact_traffic.shape)
print("\nAll rows:")
print(fact_traffic)

unmatched = fact_traffic[fact_traffic["zone_id"].isna()]
if len(unmatched) > 0:
    print(f"\nWARNING: {len(unmatched)} rows have no matching zone!")

fact_traffic.to_sql("fact_traffic", conn, if_exists="replace", index=False)
conn.close()

print("\nSaved fact_traffic table to mobility.db")
