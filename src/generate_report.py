import pandas as pd
import sqlite3
from datetime import datetime

conn = sqlite3.connect("data/processed/mobility.db")

kpis = pd.read_sql(
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

top_congested = pd.read_sql(
    """
    SELECT zone_name, ROUND(AVG(congestion_index), 2) as avg_congestion
    FROM fact_traffic_enriched
    GROUP BY zone_name
    ORDER BY avg_congestion DESC
    LIMIT 3
""",
    conn,
)

worst_routes = pd.read_sql(
    """
    SELECT pickup_zone, dropoff_zone, ROUND(AVG(speed_kmh), 1) as avg_speed_kmh
    FROM fact_trips_enriched
    GROUP BY pickup_zone, dropoff_zone
    HAVING COUNT(*) >= 3
    ORDER BY avg_speed_kmh ASC
    LIMIT 3
""",
    conn,
)

alert_count = pd.read_sql(
    """
    SELECT COUNT(*) as n FROM fact_traffic_enriched WHERE congestion_index > 0.75
""",
    conn,
).iloc[0]["n"]

conn.close()

report_date = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

report = f"""# Bengaluru Mobility Report
Generated: {report_date}

## Key Metrics
- Total trips analyzed: {kpis.iloc[0]['total_trips']}
- Average speed: {kpis.iloc[0]['avg_speed_kmh']} km/h
- Average trip duration: {kpis.iloc[0]['avg_duration_min']} minutes
- Average fare: ₹{kpis.iloc[0]['avg_fare']}

## Most Congested Zones
"""
for _, row in top_congested.iterrows():
    report += f"- {row['zone_name']}: {row['avg_congestion']} avg congestion index\n"

report += "\n## Slowest Routes (candidates for intervention)\n"
for _, row in worst_routes.iterrows():
    report += f"- {row['pickup_zone']} → {row['dropoff_zone']}: {row['avg_speed_kmh']} km/h average\n"

report += f"\n## Alerts\n- {alert_count} traffic readings exceeded the 0.75 congestion threshold\n"

filename = f"reports/mobility_report_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
import os

os.makedirs("reports", exist_ok=True)
with open(filename, "w") as f:
    f.write(report)

print(f"Report generated: {filename}")
print("\n" + report)
