-- models/marts/core/fct_image_detections.sql
{{
  config(
    materialized='table',
    schema='analytics_analytics'
  )
}}

WITH base AS (
    SELECT
        m.message_id,
        m.image_path,
        d.detected_object_class,
        d.confidence_score
    FROM {{ ref('stg_telegram_messages') }} m
    JOIN {{ source('analytics', 'fct_image_detections') }} d
        ON m.message_id = d.message_id
    WHERE m.is_image_flag = TRUE
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['message_id', 'detected_object_class']) }} AS detection_key,
    message_id,
    detected_object_class,
    -- Cast the result of the multiplication to NUMERIC before rounding
    ROUND((confidence_score * 100)::NUMERIC, 2) AS confidence_score_pct,
    -- OR, if you prefer, cast the confidence_score first:
    -- ROUND((confidence_score::NUMERIC * 100), 2) AS confidence_score_pct,
    image_path
FROM base