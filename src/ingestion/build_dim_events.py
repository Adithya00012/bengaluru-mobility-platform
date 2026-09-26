import pandas as pd
import sqlite3

events = [
    {
        "event_date": "2026-09-15",
        "zone_name": "Indiranagar",
        "event_name": "Ganesh Chaturthi street procession",
        "event_type": "Festival",
    },
    {
        "event_date": "2026-09-19",
        "zone_name": "Koramangala",
        "event_name": "Tech meetup conference",
        "event_type": "Conference",
    },
    {
        "event_date": "2026-09-23",
        "zone_name": "MG Road / Central",
        "event_name": "Cricket match - fan gathering",
        "event_type": "Sports",
    },
    {
        "event_date": "2026-09-27",
        "zone_name": "Whitefield",
        "event_name": "Music festival",
        "event_type": "Concert",
    },
]

dim_events = pd.DataFrame(events)
dim_events["date_id"] = (
    pd.to_datetime(dim_events["event_date"]).dt.strftime("%Y%m%d").astype(int)
)

conn = sqlite3.connect("data/processed/mobility.db")

dim_location = pd.read_sql("SELECT zone_id, zone_name FROM dim_location", conn)
dim_events = dim_events.merge(dim_location, on="zone_name", how="left")

dim_events = dim_events[["date_id", "zone_id", "zone_name", "event_name", "event_type"]]

print("dim_events:")
print(dim_events)

dim_events.to_sql("dim_events", conn, if_exists="replace", index=False)
conn.close()

print("\nSaved dim_events table to mobility.db")
