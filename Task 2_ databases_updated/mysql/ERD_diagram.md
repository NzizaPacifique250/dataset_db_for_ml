```mermaid
erDiagram
    traffic {
        int primary_id PK
        float rain_1h
        float snow_1h
        int clouds_all
        int temp
        int traffic_volume
        int lag_1
        int lag_24
        int lag_168
        int rolling_mean_24
        int rolling_mean_168
        int datetime_id FK
        int holiday_id FK
        int weather_id FK
    }

    datetime_info {
        int datetime_id PK
        datetime date_time
        int year
        int month
        int day
        int hour
        int is_weekend
        int day_of_week
    }

    holiday_info {
        int holiday_id PK
        varchar holiday_name
    }

    weather_info {
        int weather_id PK
        varchar weather_main
    }

    traffic ||--|| datetime_info : "datetime_id FK"
    traffic ||--|| holiday_info : "holiday_id FK"
    traffic ||--|| weather_info : "weather_id FK"