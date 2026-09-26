import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

result = pd.read_sql(
    """
SELECT
    de.date_id, de.zone_name, de.event_name,
    ROUND(AVG(ft.congestion_index), 2) as avg_congestion_on_event_day
FROM dim_events de
JOIN fact_traffic ft ON de.date_id = ft.date_id AND de.zone_id = ft.zone_id
GROUP BY de.date_id, de.zone_name, de.event_name
""",
    conn,
)

zone_baselines = pd.read_sql(
    """
SELECT zone_name, ROUND(AVG(congestion_index), 2) as zone_baseline_congestion
FROM fact_traffic_enriched GROUP BY zone_name
""",
    conn,
)
conn.close()

result = result.merge(zone_baselines, on="zone_name")
result["difference"] = (
    result["avg_congestion_on_event_day"] - result["zone_baseline_congestion"]
)

print("=== Event Impact on Congestion ===")
print(result)
