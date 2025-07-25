from dagster import job
from ops import (
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations,
    run_yolo_enrichment
)

@job
def telegram_analytics_pipeline():
    data = scrape_telegram_data()
    loaded = load_raw_to_postgres(data)
    dbt = run_dbt_transformations()
    yolo = run_yolo_enrichment(dbt)