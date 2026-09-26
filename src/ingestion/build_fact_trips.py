import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

trips = pd.read_csv("data/processed/cleaned_trips.csv")
dim_location = pd.read_sql("SELECT * FROM dim_location", conn)


def find_nearest_zone(lat, lon, zones_df):
    distances = (
        (zones_df["center_lat"] - lat) ** 2 + (zones_df["center_lon"] - lon) ** 2
    ) ** 0.5
    nearest_index = distances.idxmin()  
    return zones_df.loc[nearest_index, "zone_id"]


trips["pickup_zone_id"] = trips.apply(
    lambda row: find_nearest_zone(row["pickup_lat"], row["pickup_lon"], dim_location),
    axis=1,
)
trips["dropoff_zone_id"] = trips.apply(
    lambda row: find_nearest_zone(row["dropoff_lat"], row["dropoff_lon"], dim_location),
    axis=1,
)

trips["pickup_time"] = pd.to_datetime(trips["pickup_time"])
trips["dropoff_time"] = pd.to_datetime(trips["dropoff_time"])

trips["date_id"] = trips["pickup_time"].dt.strftime("%Y%m%d").astype(int)
trips["time_id"] = trips["pickup_time"].dt.hour

trips["speed_kmh"] = trips["distance_km"] / (trips["duration_min"] / 60)

fact_trips = trips[
    [
        "trip_id",
        "date_id",
        "time_id",
        "pickup_zone_id",
        "dropoff_zone_id",
        "distance_km",
        "duration_min",
        "speed_kmh",
        "fare",
    ]
]

print("fact_trips shape:", fact_trips.shape)
print("\nSample rows:")
print(fact_trips.head(10))

fact_trips.to_sql("fact_trips", conn, if_exists="replace", index=False)
conn.close()

print("\nSaved fact_trips table to mobility.db")
