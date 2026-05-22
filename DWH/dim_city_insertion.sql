-- =====================================================
-- Telbs EH DWH Insertion Script
-- Source Schema: telbs_eh_final_proj
-- Target Schema: telbs_eh_dwh
-- =====================================================

USE telbs_eh_dwh;

-- =====================================================
-- 1. Load / Update dim_city
-- Source: telbs_eh_final_proj.gold_city_state_lat_long
-- =====================================================

INSERT INTO telbs_eh_dwh.dim_city (
    global_city_id,
    table_city_id,
    city_name,
    state_name,
    country_code,
    lat,
    lon
)
SELECT DISTINCT
    global_id AS global_city_id,
    id AS table_city_id,
    city_name,
    state_name,
    country_code,
    lat,
    lang AS lon
FROM telbs_eh_final_proj.gold_city_state_lat_long
WHERE global_id IS NOT NULL
ON DUPLICATE KEY UPDATE
    table_city_id = VALUES(table_city_id),
    city_name = VALUES(city_name),
    state_name = VALUES(state_name),
    country_code = VALUES(country_code),
    lat = VALUES(lat),
    lon = VALUES(lon),
    updated_at = CURRENT_TIMESTAMP;