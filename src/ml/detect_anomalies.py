import pandas as pd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")

daily_trips = pd.read_sql(
    """
    SELECT full_date, COUNT(*) as trip_count
    FROM fact_trips_enriched
    GROUP BY full_date
    ORDER BY full_date
""",
    conn,
)

mean_trips = daily_trips["trip_count"].mean()
std_trips = daily_trips["trip_count"].std()

daily_trips["z_score"] = (daily_trips["trip_count"] - mean_trips) / std_trips
daily_trips["is_anomaly"] = daily_trips["z_score"].abs() > 2

print("=== Daily Trip Volume Anomaly Detection ===")
print(f"Mean daily trips: {mean_trips:.1f}, Std dev: {std_trips:.1f}")
anomalies = daily_trips[daily_trips["is_anomaly"]]
print(f"\nAnomalous days found: {len(anomalies)}")
if len(anomalies) > 0:
    print(anomalies[["full_date", "trip_count", "z_score"]])
else:
    print(
        "(None found - trip volume was consistent across all days, which is expected for our evenly-generated synthetic data)"
    )

hourly_congestion = pd.read_sql(
    """
    SELECT full_date, hour, zone_name, congestion_index
    FROM fact_traffic_enriched
""",
    conn,
)
conn.close()

mean_congestion = hourly_congestion["congestion_index"].mean()
std_congestion = hourly_congestion["congestion_index"].std()

hourly_congestion["z_score"] = (
    hourly_congestion["congestion_index"] - mean_congestion
) / std_congestion
hourly_congestion["is_anomaly"] = hourly_congestion["z_score"].abs() > 2

print(f"\n\n=== Congestion Spike Anomaly Detection ===")
print(f"Mean congestion index: {mean_congestion:.2f}, Std dev: {std_congestion:.2f}")
congestion_anomalies = hourly_congestion[hourly_congestion["is_anomaly"]]
print(
    f"\nAnomalous readings found: {len(congestion_anomalies)} of {len(hourly_congestion)}"
)
print(
    congestion_anomalies[
        ["full_date", "hour", "zone_name", "congestion_index", "z_score"]
    ]
    .sort_values("z_score", ascending=False)
    .head(10)
)
