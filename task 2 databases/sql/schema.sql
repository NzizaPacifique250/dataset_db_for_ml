-- ============================================================
-- Metro Interstate Traffic Volume - SQL Schema
-- Database: traffic_db
-- Tables: holidays, weather_conditions, traffic_records
-- ============================================================

-- Create the database
CREATE DATABASE IF NOT EXISTS traffic_db;
USE traffic_db;

-- ============================================================
-- Table 1: holidays
-- Stores unique holiday names referenced by traffic records
-- ============================================================
CREATE TABLE IF NOT EXISTS holidays (
    holiday_id INT AUTO_INCREMENT PRIMARY KEY,
    holiday_name VARCHAR(100) NOT NULL UNIQUE
);

-- ============================================================
-- Table 2: weather_conditions
-- Stores unique weather category + description combinations
-- ============================================================
CREATE TABLE IF NOT EXISTS weather_conditions (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    weather_main VARCHAR(50) NOT NULL,
    weather_description VARCHAR(100) NOT NULL,
    UNIQUE KEY uq_weather (weather_main, weather_description)
);

-- ============================================================
-- Table 3: traffic_records
-- Main fact table storing hourly traffic observations
-- ============================================================
CREATE TABLE IF NOT EXISTS traffic_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    date_time DATETIME NOT NULL,
    temp DECIMAL(6, 2),
    rain_1h DECIMAL(8, 2),
    snow_1h DECIMAL(8, 2),
    clouds_all INT,
    traffic_volume INT,
    holiday_id INT NULL,
    weather_id INT NOT NULL,
    FOREIGN KEY (holiday_id) REFERENCES holidays(holiday_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (weather_id) REFERENCES weather_conditions(weather_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_date_time (date_time),
    INDEX idx_traffic_volume (traffic_volume)
);
