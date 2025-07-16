from dagster import Definitions
from jobs import telegram_analytics_pipeline
from resources import (
    postgres_resource,
    telegram_scraper_resource,
    dbt_resource
)
from schedules import daily_telegram_analytics_schedule

defs = Definitions(
    jobs=[telegram_analytics_pipeline],
    schedules=[daily_telegram_analytics_schedule],
    resources={
        "postgres": postgres_resource.configured({
            "connection_string": "postgresql://user:password@localhost:5432/telegram_analytics"
        }),
        "telegram_scraper": telegram_scraper_resource,
        "dbt": dbt_resource
    }
)