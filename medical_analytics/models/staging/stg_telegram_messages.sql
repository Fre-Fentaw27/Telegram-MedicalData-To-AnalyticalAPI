{{
  config(
    materialized='view',
    schema='staging'
  )
}}

SELECT
    id AS message_id,
    date AS message_date,
    text AS message_text,
    views AS view_count,
    channel AS channel_name,
    has_media AS has_media_flag,
    is_image AS is_image_flag,
    image_path,
    scraped_at,
    -- Extract additional fields from raw_data JSON if needed
    raw_data->>'forwarded_from' AS forwarded_from,
    raw_data->>'replies' AS reply_count,
    raw_data->>'forwards' AS forward_count
FROM {{ source('raw', 'telegram_messages') }}