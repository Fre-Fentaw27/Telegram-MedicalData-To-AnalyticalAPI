{{
  config(
    materialized='table',
    schema='analytics'
  )
}}

SELECT
    m.message_id,
    {{ dbt_utils.generate_surrogate_key(['m.channel_name']) }} AS channel_key,
    {{ dbt_utils.generate_surrogate_key(["date_trunc('day', m.message_date)"]) }} AS date_key,
    m.message_date,
    m.message_text,
    LENGTH(m.message_text) AS message_length,
    m.view_count,
    m.has_media_flag,
    m.is_image_flag,
    m.image_path,
    m.forwarded_from,
    m.reply_count::INTEGER AS reply_count,
    m.forward_count::INTEGER AS forward_count,
    CASE 
        WHEN m.message_text ~* 'covid' THEN TRUE 
        ELSE FALSE 
    END AS mentions_covid,
    CASE 
        WHEN m.message_text ~* 'vaccine' THEN TRUE 
        ELSE FALSE 
    END AS mentions_vaccine,
    m.scraped_at
FROM {{ ref('stg_telegram_messages') }} m