import pandas as pd
import numpy as np
import sqlite3

date_range = pd.date_range(start="2026-01-01", end="2026-12-31", freq="D")

np.random.seed(42)


def simulate_rain(date):
    monsoon_months = [6, 7, 8, 9]
    rain_chance = 0.6 if date.month in monsoon_months else 0.15
    return np.random.random() < rain_chance


def simulate_temp(date):
    if date.month in [12, 1, 2]:
        return round(np.random.uniform(15, 25), 1) 
    elif date.month in [3, 4, 5]:
        return round(np.random.uniform(22, 35), 1)  
    else:
        return round(np.random.uniform(19, 28), 1)  


dim_weather = pd.DataFrame(
    {
        "date_id": date_range.strftime("%Y%m%d").astype(int),
        "full_date": date_range,
        "is_rain": [simulate_rain(d) for d in date_range],
        "temperature_c": [simulate_temp(d) for d in date_range],
    }
)

print("dim_weather shape:", dim_weather.shape)
print("\nSample rows:")
print(dim_weather.head(10))

conn = sqlite3.connect("data/processed/mobility.db")
dim_weather.to_sql("dim_weather", conn, if_exists="replace", index=False)
conn.close()

print("\nSaved dim_weather table to mobility.db")
