import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)  

zones = {
    "MG Road / Central": (12.9716, 77.5946),
    "Indiranagar": (12.9784, 77.6408),
    "Whitefield": (12.9698, 77.7500),
    "Koramangala": (12.9352, 77.6146),
    "Jayanagar": (12.9165, 77.6101),
    "Hebbal": (13.0067, 77.5648),
    "Electronic City": (12.8452, 77.6602),
    "HSR Layout": (12.9121, 77.6446),
}
zone_names = list(zones.keys())


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371  
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def random_pickup_time(day_offset):
    hour_weights = [
        1,
        1,
        1,
        1,
        1,
        2,
        3,
        5,
        8,
        7,
        4,
        3,
        3,
        3,
        3,
        3,
        4,
        7,
        8,
        7,
        5,
        3,
        2,
        1,
    ]  
    hour = np.random.choice(range(24), p=np.array(hour_weights) / sum(hour_weights))
    minute = np.random.randint(0, 60)
    base_date = datetime(2026, 9, 1) + timedelta(days=day_offset)
    return base_date.replace(hour=hour, minute=minute, second=0)


def generate_trip(trip_id, day_offset):
    pickup_zone, dropoff_zone = np.random.choice(zone_names, size=2, replace=False)
    p_lat, p_lon = zones[pickup_zone]
    d_lat, d_lon = zones[dropoff_zone]

    p_lat += np.random.uniform(-0.01, 0.01)
    p_lon += np.random.uniform(-0.01, 0.01)
    d_lat += np.random.uniform(-0.01, 0.01)
    d_lon += np.random.uniform(-0.01, 0.01)

    pickup_time = random_pickup_time(day_offset)
    distance_km = round(haversine_km(p_lat, p_lon, d_lat, d_lon), 1)

    is_peak = pickup_time.hour in [8, 9, 10, 17, 18, 19, 20]
    base_speed = np.random.uniform(12, 18) if is_peak else np.random.uniform(20, 32)
    duration_min = round((distance_km / base_speed) * 60 + np.random.uniform(-3, 3), 1)
    duration_min = max(duration_min, 2)  

    dropoff_time = pickup_time + timedelta(minutes=duration_min)
    fare = round(distance_km * np.random.uniform(20, 28) + 20, 0)

    return {
        "trip_id": trip_id,
        "pickup_time": pickup_time,
        "dropoff_time": dropoff_time,
        "pickup_lat": round(p_lat, 4),
        "pickup_lon": round(p_lon, 4),
        "dropoff_lat": round(d_lat, 4),
        "dropoff_lon": round(d_lon, 4),
        "distance_km": distance_km,
        "fare": fare,
    }


trips = []
trip_id = 1
for day in range(30):
    num_trips_today = np.random.randint(12, 22)  
    for _ in range(num_trips_today):
        trips.append(generate_trip(trip_id, day))
        trip_id += 1

df = pd.DataFrame(trips)
print(f"Generated {len(df)} synthetic trips across 30 days")
print(df.head())

df.to_csv("data/raw/sample_trips.csv", index=False)
print("\nSaved to data/raw/sample_trips.csv")
