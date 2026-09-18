import pandas as pd

df = pd.read_csv("data/raw/sample_trips.csv")

print("Before cleaning:", df.shape)

df["pickup_time"] = pd.to_datetime(df["pickup_time"])
df["dropoff_time"] = pd.to_datetime(df["dropoff_time"])

df["duration_min"] = (df["dropoff_time"] - df["pickup_time"]).dt.total_seconds() / 60

df = df.dropna(subset=["dropoff_time"])

df = df[df["duration_min"] > 0]

print("After cleaning:", df.shape)
print("\nCleaned data:")
print(df[["trip_id", "pickup_time", "dropoff_time", "duration_min", "fare"]])

df.to_csv("data/processed/cleaned_trips.csv", index=False)
print("\nSaved cleaned_trips.csv to data/processed/")
