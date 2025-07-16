from dagster import Definitions
from jobs import telegram_analytics_pipeline
from resources import postgres_resource, telegram_scraper
from schedules import daily_ingestion_schedule

defs = Definitions(
    jobs=[telegram_analytics_pipeline],
    schedules=[daily_ingestion_schedule],
    resources={
        "postgres": postgres_resource,
        "telegram_scraper": telegram_scraper
    }
)