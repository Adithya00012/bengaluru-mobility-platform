import pandas as pd
import sqlite3

date_range = pd.date_range(start="2026-01-01", end="2026-12-31", freq="D")

karnataka_holidays_2026 = {
    "2026-01-01": "New Year's Day",
    "2026-01-14": "Makara Sankranti",
    "2026-01-26": "Republic Day",
    "2026-03-19": "Ugadi",
    "2026-03-21": "Eid-ul-Fitr",
    "2026-03-31": "Mahavir Jayanti",
    "2026-04-03": "Good Friday",
    "2026-04-14": "Dr. B.R. Ambedkar Jayanti",
    "2026-04-20": "Basava Jayanti",
    "2026-05-01": "May Day",
    "2026-05-27": "Bakrid (Eid-ul-Adha)",
    "2026-06-26": "Muharram",
    "2026-08-15": "Independence Day",
    "2026-08-25": "Eid-e-Milad",
    "2026-09-15": "Ganesh Chaturthi",
    "2026-10-02": "Gandhi Jayanti",
    "2026-10-20": "Vijayadashami (Dasara)",
    "2026-11-01": "Kannada Rajyotsava",
    "2026-11-08": "Diwali",
    "2026-12-25": "Christmas Day",
}

dim_date = pd.DataFrame({
    "date_id": date_range.strftime("%Y%m%d").astype(int),
    "full_date": date_range,
    "year": date_range.year,
    "month": date_range.month,
    "day": date_range.day,
    "day_of_week": date_range.day_name(),
    "is_weekend": date_range.dayofweek >= 5,
})

date_strings = date_range.strftime("%Y-%m-%d")
dim_date["is_holiday"] = date_strings.isin(karnataka_holidays_2026.keys())
dim_date["holiday_name"] = [karnataka_holidays_2026.get(d, None) for d in date_strings]

print("dim_date shape:", dim_date.shape)
print(f"\nHolidays found: {dim_date['is_holiday'].sum()}")
print("\nSample holiday rows:")
print(dim_date[dim_date["is_holiday"]][["full_date", "day_of_week", "holiday_name"]].head(10))

conn = sqlite3.connect("data/processed/mobility.db")
dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)
conn.close()

print("\nSaved dim_date table to mobility.db")