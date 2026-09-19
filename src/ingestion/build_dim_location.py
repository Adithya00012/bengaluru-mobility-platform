import pandas as pd
import sqlite3

zones = [
    {
        "zone_id": 1,
        "zone_name": "MG Road / Central",
        "center_lat": 12.9716,
        "center_lon": 77.5946,
    },
    {
        "zone_id": 2,
        "zone_name": "Indiranagar",
        "center_lat": 12.9784,
        "center_lon": 77.6408,
    },
    {
        "zone_id": 3,
        "zone_name": "Whitefield",
        "center_lat": 12.9698,
        "center_lon": 77.7500,
    },
    {
        "zone_id": 4,
        "zone_name": "Koramangala",
        "center_lat": 12.9352,
        "center_lon": 77.6146,
    },
    {
        "zone_id": 5,
        "zone_name": "Jayanagar",
        "center_lat": 12.9165,
        "center_lon": 77.6101,
    },
    {"zone_id": 6, "zone_name": "Hebbal", "center_lat": 13.0067, "center_lon": 77.5648},
    {
        "zone_id": 7,
        "zone_name": "Electronic City",
        "center_lat": 12.8452,
        "center_lon": 77.6602,
    },
    {
        "zone_id": 8,
        "zone_name": "HSR Layout",
        "center_lat": 12.9121,
        "center_lon": 77.6446,
    },
]

dim_location = pd.DataFrame(zones)

print("dim_location shape:", dim_location.shape)
print("\nAll zones:")
print(dim_location)

conn = sqlite3.connect("data/processed/mobility.db")
dim_location.to_sql("dim_location", conn, if_exists="replace", index=False)
conn.close()

print("\nSaved dim_location table to mobility.db")
