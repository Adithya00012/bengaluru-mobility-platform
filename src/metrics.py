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
