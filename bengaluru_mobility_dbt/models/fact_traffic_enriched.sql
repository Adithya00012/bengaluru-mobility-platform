select
    dt.full_date,
    dt.day_of_week,
    dt.is_weekend,
    dt.is_holiday,
    dt.holiday_name,
    tm.hour,
    tm.period_of_day,
    tm.is_peak_hour,
    loc.zone_name,
    ft.avg_speed_kmh,
    ft.congestion_index

from {{ source('mobility_raw', 'fact_traffic') }} ft
join {{ source('mobility_raw', 'dim_date') }} dt on ft.date_id = dt.date_id
join {{ source('mobility_raw', 'dim_time') }} tm on ft.time_id = tm.time_id
join {{ source('mobility_raw', 'dim_location') }} loc on ft.zone_id = loc.zone_id