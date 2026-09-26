import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

kpi_summary = pd.read_sql(
    """
    SELECT
        COUNT(*) as total_trips,
        ROUND(AVG(speed_kmh), 1) as avg_speed_kmh,
        ROUND(AVG(duration_min), 1) as avg_duration_min,
        ROUND(AVG(fare), 0) as avg_fare
    FROM fact_trips_enriched
""",
    conn,
)

zone_congestion = pd.read_sql(
    """
    SELECT zone_name, ROUND(AVG(congestion_index), 2) as avg_congestion
    FROM fact_traffic_enriched GROUP BY zone_name ORDER BY avg_congestion DESC
""",
    conn,
)

route_performance = pd.read_sql(
    """
    SELECT pickup_zone, dropoff_zone, COUNT(*) as trip_count, ROUND(AVG(speed_kmh),1) as avg_speed_kmh
    FROM fact_trips_enriched GROUP BY pickup_zone, dropoff_zone HAVING trip_count >= 3
    ORDER BY avg_speed_kmh ASC
""",
    conn,
)

weather_impact = pd.read_sql(
    """
    SELECT is_rain, is_holiday, ROUND(AVG(speed_kmh),1) as avg_speed_kmh, COUNT(*) as trip_count
    FROM fact_trips_enriched GROUP BY is_rain, is_holiday
""",
    conn,
)

conn.close()

with pd.ExcelWriter(
    "reports/mobility_scenario_analysis.xlsx", engine="openpyxl"
) as writer:
    kpi_summary.to_excel(writer, sheet_name="KPI Summary", index=False)
    zone_congestion.to_excel(writer, sheet_name="Zone Congestion", index=False)
    route_performance.to_excel(writer, sheet_name="Route Performance", index=False)
    weather_impact.to_excel(writer, sheet_name="Weather-Holiday Impact", index=False)

print("Exported reports/mobility_scenario_analysis.xlsx with 4 sheets")
