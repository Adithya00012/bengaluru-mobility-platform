# Database Schema

## Entity-Relationship Diagram

```mermaid
erDiagram
    dim_date ||--o{ fact_trips : "date_id"
    dim_time ||--o{ fact_trips : "time_id"
    dim_location ||--o{ fact_trips : "pickup_zone_id"
    dim_location ||--o{ fact_trips : "dropoff_zone_id"
    dim_date ||--o{ fact_traffic : "date_id"
    dim_time ||--o{ fact_traffic : "time_id"
    dim_location ||--o{ fact_traffic : "zone_id"

    dim_date {
        int date_id PK
        date full_date
        boolean is_weekend
        boolean is_holiday
    }
    dim_time {
        int time_id PK
        int hour
        boolean is_peak_hour
    }
    dim_location {
        int zone_id PK
        string zone_name
    }
    fact_trips {
        int trip_id PK
        int date_id FK
        int time_id FK
        int pickup_zone_id FK
        int dropoff_zone_id FK
        float distance_km
        float duration_min
    }
    fact_traffic {
        int date_id FK
        int time_id FK
        int zone_id FK
        float congestion_index
    }
```

## Design notes
This is a **star schema**: two fact tables (`fact_trips`, `fact_traffic`) each connect to shared dimension tables (`dim_date`, `dim_time`, `dim_location`). `fact_trips` joins `dim_location` **twice** — once for pickup zone, once for dropoff zone — since a single trip references two different locations. `dim_weather` (not shown above) joins to both fact tables via `date_id`.

See `data_dictionary.md` for full column-level detail on every table.