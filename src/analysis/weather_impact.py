import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

query = """
SELECT
    is_rain,
    COUNT(*) AS trip_count,
    ROUND(AVG(speed_kmh), 1) AS avg_speed_kmh,
    ROUND(AVG(duration_min), 1) AS avg_duration_min
FROM fact_trips_enriched
GROUP BY is_rain
"""
weather_impact = pd.read_sql(query, conn)

print("=== Trip performance: rain vs no rain ===")
print(weather_impact)

trips = pd.read_sql("SELECT * FROM fact_trips_enriched", conn)
conn.close()

correlation = trips["temperature_c"].corr(trips["speed_kmh"])
print(f"\nCorrelation between temperature and speed: {correlation:.2f}")
print("(Closer to 0 = no relationship, closer to +/-1 = strong relationship)")

print("\n=== All trips with weather context, slowest first ===")
print(
    trips[
        ["trip_id", "pickup_zone", "is_rain", "temperature_c", "speed_kmh"]
    ].sort_values("speed_kmh")
)

# --- Holiday impact analysis ---
conn = sqlite3.connect("data/processed/mobility.db")
holiday_query = """
SELECT
    is_holiday,
    COUNT(*) AS trip_count,
    ROUND(AVG(speed_kmh), 1) AS avg_speed_kmh,
    ROUND(AVG(duration_min), 1) AS avg_duration_min,
    ROUND(AVG(fare), 0) AS avg_fare
FROM fact_trips_enriched
GROUP BY is_holiday
"""
holiday_impact = pd.read_sql(holiday_query, conn)
conn.close()

print("\n\n=== Trip performance: holiday vs non-holiday ===")
print(holiday_impact)

conn = sqlite3.connect("data/processed/mobility.db")
export_df = pd.read_sql(
    """
SELECT
    is_rain, is_holiday,
    speed_kmh, duration_min, fare, full_date, pickup_zone
FROM fact_trips_enriched
""",
    conn,
)
conn.close()
export_df.to_csv("data/processed/weather_holiday_for_powerbi.csv", index=False)
print(
    f"\nExported {len(export_df)} rows to data/processed/weather_holiday_for_powerbi.csv"
)
