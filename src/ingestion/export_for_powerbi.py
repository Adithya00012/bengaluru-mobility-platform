import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

query = """
SELECT
    f.trip_id,
    dt.full_date,
    dt.day_of_week,
    dt.is_weekend,
    tm.hour,
    tm.period_of_day,
    tm.is_peak_hour,
    loc.zone_name AS pickup_zone,
    w.is_rain,
    w.temperature_c,
    f.distance_km,
    f.duration_min,
    f.speed_kmh,
    f.fare
FROM fact_trips f
JOIN dim_date dt ON f.date_id = dt.date_id
JOIN dim_time tm ON f.time_id = tm.time_id
JOIN dim_location loc ON f.pickup_zone_id = loc.zone_id
JOIN dim_weather w ON f.date_id = w.date_id
"""

df = pd.read_sql(query, conn)
conn.close()

df.to_csv("data/processed/trips_for_powerbi.csv", index=False)
print(f"Exported {len(df)} rows to data/processed/trips_for_powerbi.csv")
