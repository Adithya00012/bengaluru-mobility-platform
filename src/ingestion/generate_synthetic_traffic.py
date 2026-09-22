import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

zone_names = [
    "MG Road / Central",
    "Indiranagar",
    "Whitefield",
    "Koramangala",
    "Jayanagar",
    "Hebbal",
    "Electronic City",
    "HSR Layout",
]


def generate_reading(reading_time, zone_name):
    hour = reading_time.hour
    is_peak = hour in [8, 9, 10, 17, 18, 19, 20]

    busy_zones = ["MG Road / Central", "Koramangala", "Indiranagar"]
    zone_busyness = 0.15 if zone_name in busy_zones else 0.0

    base_congestion = 0.55 if is_peak else 0.25
    congestion_index = np.clip(
        base_congestion + zone_busyness + np.random.normal(0, 0.12), 0.05, 0.98
    )

    avg_speed_kmh = round(
        max(5, 30 * (1 - congestion_index) + np.random.normal(0, 2)), 1
    )

    return {
        "reading_time": reading_time,
        "zone_name": zone_name,
        "avg_speed_kmh": avg_speed_kmh,
        "congestion_index": round(congestion_index, 2),
    }


readings = []
for day in range(30):
    base_date = datetime(2026, 9, 1) + timedelta(days=day)
    for hour in range(6, 22):  # readings from 6am to 9pm
        reading_time = base_date.replace(hour=hour)
        for zone in zone_names:
            readings.append(generate_reading(reading_time, zone))

df = pd.DataFrame(readings)
print(f"Generated {len(df)} synthetic traffic readings")
print(df.head(10))

df.to_csv("data/raw/sample_traffic.csv", index=False)
print("\nSaved to data/raw/sample_traffic.csv")
