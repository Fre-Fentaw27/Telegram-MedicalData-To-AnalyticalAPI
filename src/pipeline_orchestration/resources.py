import os
from dagster import resource
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

class PostgresResource:
    def __init__(self):
        self.connection_string = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        self.engine = create_engine(self.connection_string)

    def get_engine(self):
        return self.engine

@resource
def postgres_resource(_):
    return PostgresResource()

class TelegramScraperResource:
    def scrape(self, channel_name: str):
        # Your scraping logic here
        return f"Scraped data from {channel_name}"

@resource
def telegram_scraper(_):
    return TelegramScraperResource()