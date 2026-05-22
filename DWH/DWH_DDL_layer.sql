-- =====================================================
-- Telbs EH Data Warehouse Schema
-- Purpose: Historical weather / temperature analysis
-- =====================================================

CREATE DATABASE IF NOT EXISTS telbs_eh_dwh;
USE telbs_eh_dwh;

-- =====================================================
-- 1. Dimension: City
-- Grain: one row per global city
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_city (
    city_key INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    global_city_id INT NOT NULL,
    table_city_id VARCHAR(20) DEFAULT NULL,

    city_name VARCHAR(150) DEFAULT NULL,
    state_name VARCHAR(150) DEFAULT NULL,
    country_code VARCHAR(50) DEFAULT NULL,

    lat DECIMAL(10,8) DEFAULT NULL,
    lon DECIMAL(11,8) DEFAULT NULL,

    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_dim_city_global_city_id (global_city_id)
) ;


-- =====================================================
-- 2. Dimension: Date
-- Grain: one row per calendar date
-- date_key format: YYYYMMDD
-- Example: 20260522
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY NOT NULL,
    full_date DATE NOT NULL,

    day INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    UNIQUE KEY uq_dim_date_full_date (full_date)
) ;


-- =====================================================
-- 3. Fact: Actual Weather Observation
-- Grain: one row per city per actual collection datetime
-- This is the main table for historical temperatures.
-- =====================================================

CREATE TABLE IF NOT EXISTS fact_weather_observation (
    weather_fact_id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    
    city_key INT NOT NULL,
    global_city_id INT NOT NULL,
    date_key INT NOT NULL,
    
    observation_datetime DATETIME NOT NULL,
    load_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    temp DECIMAL(6,2) DEFAULT NULL,
    feels_like DECIMAL(6,2) DEFAULT NULL,
    humidity INT DEFAULT NULL,
    wind_speed DECIMAL(8,2) DEFAULT NULL,
    visibility INT DEFAULT NULL,
    weather_desc VARCHAR(150) DEFAULT NULL,
    sunrise DATETIME DEFAULT NULL,
    sunset DATETIME DEFAULT NULL,
    
    source_system VARCHAR(100) DEFAULT 'OpenWeather_Current_API',

    UNIQUE KEY uq_fact_weather_city_observation (
        global_city_id,
        observation_datetime
    ),

    KEY idx_fact_weather_city_key (city_key),
    KEY idx_fact_weather_global_city_id (global_city_id),
    KEY idx_fact_weather_date_key (date_key),
    KEY idx_fact_weather_observation_datetime (observation_datetime),
    KEY idx_fact_weather_city_datetime (global_city_id, observation_datetime),

    CONSTRAINT fk_fact_weather_observation_city
        FOREIGN KEY (city_key)
        REFERENCES dim_city (city_key),

    CONSTRAINT fk_fact_weather_observation_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date (date_key)
) ;


-- =====================================================
-- 4. Fact: Forecast Weather
-- Grain: one row per city per forecast run per forecasted datetime
-- Use this if you want to analyze forecast history later.
-- =====================================================

CREATE TABLE IF NOT EXISTS fact_weather_forecast (
    forecast_fact_id BIGINT PRIMARY KEY NOT NULL  AUTO_INCREMENT,

    city_key INT NOT NULL,
    global_city_id INT NOT NULL,
    forecast_date_key INT NOT NULL,

    forecast_run_datetime DATETIME NOT NULL,
    forecast_for_datetime DATETIME NOT NULL,
    load_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    temp DECIMAL(6,2) DEFAULT NULL,
    feels_like DECIMAL(6,2) DEFAULT NULL,
    humidity INT DEFAULT NULL,
    wind_speed DECIMAL(8,2) DEFAULT NULL,
    weather_desc VARCHAR(150) DEFAULT NULL,
    sunrise DATETIME DEFAULT NULL,
    sunset DATETIME DEFAULT NULL,

    source_system VARCHAR(100) DEFAULT 'OpenWeather_Forecast_API',

    UNIQUE KEY uq_fact_forecast_city_run_target (
        global_city_id,
        forecast_run_datetime,
        forecast_for_datetime
    ),

    KEY idx_fact_forecast_city_key (city_key),
    KEY idx_fact_forecast_global_city_id (global_city_id),
    KEY idx_fact_forecast_date_key (forecast_date_key),
    KEY idx_fact_forecast_for_datetime (forecast_for_datetime),
    KEY idx_fact_forecast_city_target_datetime (global_city_id, forecast_for_datetime),

    CONSTRAINT fk_fact_weather_forecast_city
        FOREIGN KEY (city_key)
        REFERENCES dim_city (city_key),

    CONSTRAINT fk_fact_weather_forecast_date
        FOREIGN KEY (forecast_date_key)
        REFERENCES dim_date (date_key)
) ;