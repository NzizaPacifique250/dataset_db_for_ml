-- ============================================================
-- Metro Interstate Traffic Volume - SQL Queries
-- ============================================================

USE traffic_db;

-- ============================================================
-- Query 1: Average traffic volume by weather condition
-- Shows how different weather types affect traffic flow
-- ============================================================
SELECT
    w.weather_main,
    ROUND(AVG(tr.traffic_volume), 0) AS avg_traffic,
    COUNT(*) AS record_count
FROM traffic_records tr
JOIN weather_conditions w ON tr.weather_id = w.weather_id
GROUP BY w.weather_main
ORDER BY avg_traffic DESC;

-- ============================================================
-- Query 2: Traffic records within a specific date range
-- Retrieves hourly traffic data for a given period
-- ============================================================
SELECT
    tr.date_time,
    tr.temp,
    tr.traffic_volume,
    w.weather_main,
    w.weather_description,
    h.holiday_name
FROM traffic_records tr
JOIN weather_conditions w ON tr.weather_id = w.weather_id
LEFT JOIN holidays h ON tr.holiday_id = h.holiday_id
WHERE tr.date_time BETWEEN '2013-06-01 00:00:00' AND '2013-06-01 23:59:59'
ORDER BY tr.date_time;

-- ============================================================
-- Query 3: Compare average traffic on holidays vs non-holidays
-- Analyzes whether holidays impact traffic volume
-- ============================================================
SELECT
    CASE
        WHEN tr.holiday_id IS NOT NULL THEN 'Holiday'
        ELSE 'Non-Holiday'
    END AS day_type,
    ROUND(AVG(tr.traffic_volume), 0) AS avg_traffic,
    MIN(tr.traffic_volume) AS min_traffic,
    MAX(tr.traffic_volume) AS max_traffic,
    COUNT(*) AS record_count
FROM traffic_records tr
GROUP BY day_type;

-- ============================================================
-- Query 4: Get the latest (most recent) traffic record
-- Useful for real-time monitoring dashboards
-- ============================================================
SELECT
    tr.record_id,
    tr.date_time,
    tr.temp,
    tr.rain_1h,
    tr.snow_1h,
    tr.clouds_all,
    tr.traffic_volume,
    w.weather_main,
    w.weather_description,
    h.holiday_name
FROM traffic_records tr
JOIN weather_conditions w ON tr.weather_id = w.weather_id
LEFT JOIN holidays h ON tr.holiday_id = h.holiday_id
ORDER BY tr.date_time DESC
LIMIT 1;
