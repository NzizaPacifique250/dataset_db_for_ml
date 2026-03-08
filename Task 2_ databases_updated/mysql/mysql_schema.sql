CREATE DATABASE IF NOT EXISTS traffic_db;
USE traffic_db;

CREATE TABLE holiday_info (
    holiday_id INT PRIMARY KEY,
    holiday VARCHAR(50) NOT NULL
);

CREATE TABLE weather_info (
    weather_id INT PRIMARY KEY,
    weather_main VARCHAR(50) NOT NULL
);

CREATE TABLE datetime_info (
    datetime_id INT PRIMARY KEY,
    date_time DATETIME NOT NULL,
    year INT,
    month INT,
    day INT,
    day_of_week INT,
    hour INT,

    is_weekend TINYINT
);

CREATE TABLE traffic (
    primary_id INT PRIMARY KEY,
    temp FLOAT,
    rain_1h FLOAT,
    snow_1h FLOAT,
    clouds_all INT,
    datetime_id INT,
    holiday_id INT,
    weather_id INT,
    traffic_volume INT,
    lag_1 INT,
    lag_24 INT,
    lag_168 INT,
    rolling_mean_24 DECIMAL(10,2),
    rolling_mean_168 DECIMAL(10,2),

    FOREIGN KEY (datetime_id) REFERENCES datetime_info(datetime_id),
    FOREIGN KEY (holiday_id) REFERENCES holiday_info(holiday_id),
    FOREIGN KEY (weather_id) REFERENCES weather_info(weather_id)
);