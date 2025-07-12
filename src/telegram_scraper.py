import os
import sys
import json
import time
import asyncio
from datetime import datetime
from pathlib import Path
from loguru import logger
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

# Configure logging
logger.add("logs/scraping.log", rotation="1 week", retention="1 month")
logger.add(sys.stderr, level="INFO")

class TelegramScraper:
    def __init__(self):
        load_dotenv()
        self.client = TelegramClient(
            'session_name',
            int(os.getenv('TG_API_ID')),
            os.getenv('TG_API_HASH')
        )
        self.channels = [
            'CheMed123',
            'lobelia4cosmetics', 
            'tikvahpharma'
        ]
        self.image_channels = [
            'CheMed123',
            'lobelia4cosmetics'
        ]
        self.base_path = Path("data/raw")
        
    async def _ensure_directories(self, channel, date_str):
        """Create necessary directories for storage"""
        msg_dir = self.base_path / "telegram_messages" / date_str
        img_dir = self.base_path / "images" / date_str / channel
        msg_dir.mkdir(parents=True, exist_ok=True)
        img_dir.mkdir(parents=True, exist_ok=True)
        return msg_dir, img_dir

    async def _process_message(self, message, channel, img_dir):
        """Extract relevant data from a message"""
        msg_data = {
            'id': message.id,
            'date': message.date.isoformat(),
            'text': message.text,
            'views': message.views,
            'channel': channel,
            'has_media': bool(message.media),
            'is_image': False,
            'image_path': None
        }

        if (channel in self.image_channels and 
            isinstance(message.media, MessageMediaPhoto)):
            img_path = img_dir / f"{message.id}.jpg"
            try:
                await message.download_media(file=str(img_path))
                msg_data.update({
                    'is_image': True,
                    'image_path': str(img_path.relative_to(self.base_path))
                })
                logger.info(f"Saved image {img_path.name}")
            except Exception as e:
                logger.error(f"Failed to save image: {e}")

        return msg_data

    async def scrape_channel(self, channel, limit=1000):
        """Scrape messages from a single channel"""
        try:
            logger.info(f"Starting scrape of {channel}")
            messages = []
            
            async for message in self.client.iter_messages(channel, limit=limit):
                try:
                    date_str = message.date.strftime('%Y-%m-%d')
                    msg_dir, img_dir = await self._ensure_directories(channel, date_str)
                    
                    msg_data = await self._process_message(message, channel, img_dir)
                    messages.append(msg_data)
                    
                    # Rate limiting
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error processing message {message.id}: {e}")
                    continue

            # Save messages to JSON
            output_path = msg_dir / f"{channel}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            
            logger.success(f"Saved {len(messages)} messages from {channel} to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to scrape {channel}: {e}")

    async def scrape_all(self):
        """Scrape all configured channels"""
        await self.client.start(phone=os.getenv('PHONE'))
        
        for channel in self.channels:
            await self.scrape_channel(channel)
            await asyncio.sleep(5)  # Delay between channels
        
        await self.client.disconnect()

def main():
    scraper = TelegramScraper()
    
    # Windows-specific event loop policy
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(scraper.scrape_all())

if __name__ == '__main__':
    main()