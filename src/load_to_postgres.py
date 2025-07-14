import os
import json
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def create_raw_schema():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )
    cur = conn.cursor()
    
    # Create raw schema
    cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    
    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        id BIGINT PRIMARY KEY,
        date TIMESTAMP,
        text TEXT,
        views INTEGER,
        channel VARCHAR(255),
        has_media BOOLEAN,
        is_image BOOLEAN,
        image_path TEXT,
        raw_data JSONB,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    return conn

def load_json_files(conn):
    cur = conn.cursor()
    base_path = Path("data/raw/telegram_messages")
    
    for json_file in base_path.glob('**/*.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            messages = json.load(f)
            
            for msg in messages:
                cur.execute("""
                INSERT INTO raw.telegram_messages (
                    id, date, text, views, channel, 
                    has_media, is_image, image_path, raw_data
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) ON CONFLICT (id) DO NOTHING;
                """, (
                    msg['id'],
                    msg['date'],
                    msg['text'],
                    msg['views'],
                    msg['channel'],
                    msg['has_media'],
                    msg['is_image'],
                    msg.get('image_path'),
                    json.dumps(msg)
                ))
        
        conn.commit()
        print(f"Loaded {len(messages)} messages from {json_file}")

if __name__ == '__main__':
    conn = create_raw_schema()
    load_json_files(conn)
    conn.close()