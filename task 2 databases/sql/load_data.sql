-- ============================================================
-- Metro Interstate Traffic Volume - Data Loading Script
-- Run this AFTER schema.sql
-- ============================================================

USE traffic_db;

-- ============================================================
-- Step 1: Populate holidays table
-- ============================================================
INSERT INTO holidays (holiday_name) VALUES
    ('Christmas Day'),
    ('Columbus Day'),
    ('Independence Day'),
    ('Labor Day'),
    ('Martin Luther King Jr Day'),
    ('Memorial Day'),
    ('New Years Day'),
    ('State Fair'),
    ('Thanksgiving Day'),
    ('Veterans Day'),
    ('Washingtons Birthday');

-- ============================================================
-- Step 2: Populate weather_conditions table
-- Extract unique (weather_main, weather_description) pairs
-- ============================================================
INSERT INTO weather_conditions (weather_main, weather_description) VALUES
    ('Clear', 'sky is clear'),
    ('Clouds', 'broken clouds'),
    ('Clouds', 'few clouds'),
    ('Clouds', 'overcast clouds'),
    ('Clouds', 'scattered clouds'),
    ('Drizzle', 'drizzle'),
    ('Drizzle', 'heavy intensity drizzle'),
    ('Drizzle', 'light intensity drizzle'),
    ('Drizzle', 'shower drizzle'),
    ('Fog', 'fog'),
    ('Haze', 'haze'),
    ('Mist', 'mist'),
    ('Rain', 'freezing rain'),
    ('Rain', 'heavy intensity rain'),
    ('Rain', 'light intensity shower rain'),
    ('Rain', 'light rain'),
    ('Rain', 'light rain and snow'),
    ('Rain', 'moderate rain'),
    ('Rain', 'proximity shower rain'),
    ('Rain', 'very heavy rain'),
    ('Smoke', 'smoke'),
    ('Snow', 'heavy snow'),
    ('Snow', 'light shower snow'),
    ('Snow', 'light snow'),
    ('Snow', 'shower snow'),
    ('Snow', 'sleet'),
    ('Snow', 'snow'),
    ('Squall', 'SQUALLS'),
    ('Thunderstorm', 'proximity thunderstorm'),
    ('Thunderstorm', 'proximity thunderstorm with drizzle'),
    ('Thunderstorm', 'proximity thunderstorm with rain'),
    ('Thunderstorm', 'thunderstorm'),
    ('Thunderstorm', 'thunderstorm with drizzle'),
    ('Thunderstorm', 'thunderstorm with heavy rain'),
    ('Thunderstorm', 'thunderstorm with light drizzle'),
    ('Thunderstorm', 'thunderstorm with light rain'),
    ('Thunderstorm', 'thunderstorm with rain');

-- ============================================================
-- Step 3: Load traffic records from CSV using LOAD DATA
-- NOTE: Update the file path below to match your system
-- ============================================================

-- Create a temporary staging table to load the raw CSV
CREATE TEMPORARY TABLE temp_traffic (
    holiday VARCHAR(100),
    temp DECIMAL(6, 2),
    rain_1h DECIMAL(8, 2),
    snow_1h DECIMAL(8, 2),
    clouds_all INT,
    weather_main VARCHAR(50),
    weather_description VARCHAR(100),
    date_time VARCHAR(30),
    traffic_volume INT
);

-- Load raw CSV data into the temporary table
LOAD DATA LOCAL INFILE 'C:/Users/josue/Music/formative_1_ML_Pipeline/Metro_Interstate_Traffic_Volume.csv'
INTO TABLE temp_traffic
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(holiday, temp, rain_1h, snow_1h, clouds_all, weather_main, weather_description, date_time, traffic_volume);

-- Insert into traffic_records by joining with dimension tables
INSERT INTO traffic_records (date_time, temp, rain_1h, snow_1h, clouds_all, traffic_volume, holiday_id, weather_id)
SELECT
    STR_TO_DATE(t.date_time, '%Y-%m-%d %H:%i:%s'),
    t.temp,
    t.rain_1h,
    t.snow_1h,
    t.clouds_all,
    t.traffic_volume,
    h.holiday_id,
    w.weather_id
FROM temp_traffic t
LEFT JOIN holidays h ON t.holiday = h.holiday_name
JOIN weather_conditions w ON t.weather_main = w.weather_main
    AND t.weather_description = w.weather_description;

-- Clean up
DROP TEMPORARY TABLE temp_traffic;

-- Verify data was loaded
SELECT COUNT(*) AS total_records FROM traffic_records;
SELECT COUNT(*) AS total_holidays FROM holidays;
SELECT COUNT(*) AS total_weather_conditions FROM weather_conditions;
