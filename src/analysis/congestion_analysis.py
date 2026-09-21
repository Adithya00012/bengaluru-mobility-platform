import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

congestion_query = """
SELECT
    zone_name,
    ROUND(AVG(congestion_index), 2) AS avg_congestion,
    ROUND(AVG(avg_speed_kmh), 1) AS avg_traffic_speed,
    COUNT(*) AS reading_count
FROM fact_traffic_enriched
GROUP BY zone_name
ORDER BY avg_congestion DESC
"""
congestion_by_zone = pd.read_sql(congestion_query, conn)

print("=== Zones ranked by average congestion ===")
print(congestion_by_zone)

trips_query = "SELECT * FROM fact_trips_enriched"
trips = pd.read_sql(trips_query, conn)
conn.close()

avg_speed = trips["speed_kmh"].mean()
delay_threshold = avg_speed * 0.7 

trips["is_delayed"] = trips["speed_kmh"] < delay_threshold

print(f"\nNetwork average speed: {avg_speed:.1f} km/h")
print(f"Delay threshold (30% below average): {delay_threshold:.1f} km/h")

delayed_trips = trips[trips["is_delayed"]]
print(f"\n=== Delayed trips ({len(delayed_trips)} of {len(trips)}) ===")
print(delayed_trips[["trip_id", "pickup_zone", "hour", "speed_kmh", "is_delayed"]])
