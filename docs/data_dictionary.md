# Data Dictionary

## dim_date
| Column | Type | Description |
|---|---|---|
| date_id | integer | YYYYMMDD format, primary key |
| full_date | date | Calendar date |
| year, month, day | integer | Date components |
| day_of_week | text | e.g. "Monday" |
| is_weekend | boolean | True for Saturday/Sunday |
| is_holiday | boolean | True if a Karnataka public holiday |
| holiday_name | text | Name of the holiday, or null |

## dim_time
| Column | Type | Description |
|---|---|---|
| time_id | integer | Hour of day (0-23), primary key |
| hour | integer | Same as time_id |
| period_of_day | text | Morning/Afternoon/Evening/Night |
| is_peak_hour | boolean | True for 8-11am and 5-8pm |

## dim_location
| Column | Type | Description |
|---|---|---|
| zone_id | integer | Primary key |
| zone_name | text | Bengaluru zone/neighborhood name |
| center_lat, center_lon | float | Approximate zone center coordinates |

## dim_weather
| Column | Type | Description |
|---|---|---|
| date_id | integer | Foreign key to dim_date |
| is_rain | boolean | Simulated rain flag |
| temperature_c | float | Simulated temperature in Celsius |

## fact_trips
| Column | Type | Description |
|---|---|---|
| trip_id | integer | Primary key |
| date_id, time_id, pickup_zone_id | integer | Foreign keys to dimension tables |
| distance_km, duration_min, speed_kmh, fare | float | Trip metrics |

## fact_traffic
| Column | Type | Description |
|---|---|---|
| date_id, time_id, zone_id | integer | Foreign keys to dimension tables |
| avg_speed_kmh | float | Average vehicle speed at this reading |
| congestion_index | float (0-1) | Higher = more congested |

## Enriched models (dbt)
`fact_trips_enriched` and `fact_traffic_enriched` join the fact tables above with all relevant dimensions, producing fully readable, analysis-ready tables (used by Power BI, the ML models, and the RAG system).