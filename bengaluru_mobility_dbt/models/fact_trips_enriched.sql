select
    f.trip_id,
    dt.full_date,
    dt.day_of_week,
    dt.is_weekend,
    dt.is_holiday,
    dt.holiday_name,
    tm.hour,
    tm.period_of_day,
    tm.is_peak_hour,
    loc.zone_name as pickup_zone,
    w.is_rain,
    w.temperature_c,
    f.distance_km,
    f.duration_min,
    f.speed_kmh,
    f.fare

from {{ source('mobility_raw', 'fact_trips') }} f
join {{ source('mobility_raw', 'dim_date') }} dt on f.date_id = dt.date_id
join {{ source('mobility_raw', 'dim_time') }} tm on f.time_id = tm.time_id
join {{ source('mobility_raw', 'dim_location') }} loc on f.pickup_zone_id = loc.zone_id
join {{ source('mobility_raw', 'dim_weather') }} w on f.date_id = w.date_id