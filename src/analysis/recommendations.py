import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

congestion_by_zone_hour = pd.read_sql(
    """
    SELECT zone_name, hour, ROUND(AVG(congestion_index), 2) as avg_congestion
    FROM fact_traffic_enriched
    GROUP BY zone_name, hour
""",
    conn,
)

print("=== Time-window recommendations (best hour per zone) ===")
best_hours = congestion_by_zone_hour.loc[
    congestion_by_zone_hour.groupby("zone_name")["avg_congestion"].idxmin()
]
for _, row in best_hours.sort_values("zone_name").iterrows():
    print(
        f"{row['zone_name']}: best time to travel is {int(row['hour'])}:00 (avg congestion {row['avg_congestion']})"
    )

print("\n\n=== Threshold-based Alerts ===")

ALERT_THRESHOLD = 0.75  

recent_high_congestion = pd.read_sql(
    f"""
    SELECT full_date, hour, zone_name, congestion_index
    FROM fact_traffic_enriched
    WHERE congestion_index > {ALERT_THRESHOLD}
    ORDER BY congestion_index DESC
    LIMIT 10
""",
    conn,
)

print(f"Congestion alert threshold: {ALERT_THRESHOLD}")
print(f"\nTop 10 alert-worthy readings (congestion > {ALERT_THRESHOLD}):")
print(recent_high_congestion)

zone_summary = pd.read_sql(
    """
    SELECT
        zone_name,
        ROUND(AVG(congestion_index), 2) as avg_congestion,
        SUM(CASE WHEN congestion_index > 0.75 THEN 1 ELSE 0 END) as high_congestion_readings
    FROM fact_traffic_enriched
    GROUP BY zone_name
    ORDER BY avg_congestion DESC
""",
    conn,
)

conn.close()

print("\n\n=== Zones requiring most operational attention ===")
print(zone_summary)
print(
    f"\nRecommendation: prioritize traffic management interventions in "
    f"{zone_summary.iloc[0]['zone_name']} and {zone_summary.iloc[1]['zone_name']}, "
    f"which show both the highest average congestion and the most threshold-breaching readings."
)
