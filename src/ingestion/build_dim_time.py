import pandas as pd
import sqlite3

hours = list(range(24))


def get_period(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"


def is_peak_hour(hour):
    return (8 <= hour <= 11) or (17 <= hour <= 20)


dim_time = pd.DataFrame(
    {
        "time_id": hours,  
        "hour": hours,
        "period_of_day": [get_period(h) for h in hours],
        "is_peak_hour": [is_peak_hour(h) for h in hours],
    }
)

print("dim_time shape:", dim_time.shape)
print("\nAll rows:")
print(dim_time)

conn = sqlite3.connect("data/processed/mobility.db")
dim_time.to_sql("dim_time", conn, if_exists="replace", index=False)
conn.close()

print("\nSaved dim_time table to mobility.db")
