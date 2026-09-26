import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

query = """
SELECT
    pickup_zone,
    dropoff_zone,
    COUNT(*) as trip_count,
    ROUND(AVG(speed_kmh), 1) as avg_speed_kmh,
    ROUND(AVG(duration_min), 1) as avg_duration_min
FROM fact_trips_enriched
GROUP BY pickup_zone, dropoff_zone
HAVING trip_count >= 3
ORDER BY avg_speed_kmh ASC
"""
routes = pd.read_sql(query, conn)
conn.close()

print("=== Route-level analysis (origin-destination pairs with 3+ trips) ===")
print(routes)

print(f"\n=== Slowest routes (candidates for delay investigation) ===")
print(routes.head(5))

print(f"\n=== Fastest routes ===")
print(routes.tail(5))

routes.to_csv("data/processed/route_analysis.csv", index=False)
print("\nExported to data/processed/route_analysis.csv")
