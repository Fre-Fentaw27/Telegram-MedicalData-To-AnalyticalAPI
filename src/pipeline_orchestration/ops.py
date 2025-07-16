from dagster import op
from typing import List

@op(required_resource_keys={"telegram_scraper"})
def scrape_telegram_data(context, channels: List[str]):
    results = []
    for channel in channels:
        data = context.resources.telegram_scraper.scrape(channel)
        context.log.info(f"Scraped {len(data)} messages from {channel}")
        results.extend(data)
    return results

@op(required_resource_keys={"postgres"})
def load_raw_to_postgres(context, scraped_data):
    engine = context.resources.postgres.get_engine()
    # Implement your loading logic
    context.log.info(f"Loaded {len(scraped_data)} records to PostgreSQL")
    return len(scraped_data)

@op(required_resource_keys={"postgres"})
def run_dbt_transformations(context):
    engine = context.resources.postgres.get_engine()
    # Trigger dbt run
    context.log.info("Running dbt transformations...")
    return "dbt_run_success"

@op
def run_yolo_enrichment(context, dbt_result):
    context.log.info("Running YOLO model enrichment")
    return "enrichment_complete"