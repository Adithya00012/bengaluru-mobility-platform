import pandas as pd
import sqlite3

date_range = pd.date_range(start="2026-01-01", end="2026-12-31", freq="D")

dim_date = pd.DataFrame(
    {
        "date_id": date_range.strftime("%Y%m%d").astype(
            int
        ), 
        "full_date": date_range,
        "year": date_range.year,
        "month": date_range.month,
        "day": date_range.day,
        "day_of_week": date_range.day_name(),  
        "is_weekend": date_range.dayofweek >= 5,  
    }
)

print("dim_date shape:", dim_date.shape)
print("\nSample rows:")
print(dim_date.head())

conn = sqlite3.connect("data/processed/mobility.db")
dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)
conn.close()

print("\nSaved dim_date table to mobility.db")
