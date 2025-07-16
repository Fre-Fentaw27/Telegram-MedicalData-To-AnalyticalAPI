import os
import psycopg2
from ultralytics import YOLO
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def ensure_database_structure(conn):
    """Ensure all required tables and constraints exist"""
    with conn.cursor() as cur:
        try:
            # 1. Try to add primary key (will fail gracefully if already exists)
            try:
                cur.execute("""
                    ALTER TABLE analytics_analytics.fct_messages 
                    ADD PRIMARY KEY (message_id)
                """)
                print("Added primary key to fct_messages")
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Primary key message: {e}")

            # 2. Create detection table with proper syntax
            cur.execute("""
                CREATE TABLE IF NOT EXISTS analytics_analytics.fct_image_detections (
                    message_id BIGINT,
                    detected_object_class TEXT,
                    confidence_score FLOAT,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (message_id, detected_object_class),
                    FOREIGN KEY (message_id) REFERENCES analytics_analytics.fct_messages(message_id)
                )
            """)  # This closing parenthesis was missing
            conn.commit()
            print("Detection table ready")

        except Exception as e:
            conn.rollback()
            print(f"Database setup failed: {e}")
            raise

def detect_objects(image_path, model):
    """Run object detection on an image"""
    results = model(image_path)
    return [
        {
            "class": model.names[int(box.cls)],
            "confidence": float(box.conf)
        }
        for result in results
        for box in result.boxes
    ]

def process_images():
    model = YOLO("yolov8n.pt")
    conn = None
    
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST')
        )
        
        # Ensure database structure exists
        ensure_database_structure(conn)
        
        # Get unprocessed images
        unprocessed = pd.read_sql("""
            SELECT id as message_id, image_path 
            FROM raw.telegram_messages
            WHERE is_image = TRUE
            AND image_path IS NOT NULL
            AND id NOT IN (
                SELECT message_id 
                FROM analytics_analytics.fct_image_detections
            )
        """, conn)

        # Process each image
        for _, row in unprocessed.iterrows():
            if not os.path.exists(row['image_path']):
                continue
                
            detections = detect_objects(row['image_path'], model)
            for obj in detections:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO analytics_analytics.fct_image_detections
                        (message_id, detected_object_class, confidence_score)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (message_id, detected_object_class) DO NOTHING
                    """, (row['message_id'], obj['class'], obj['confidence']))
        
        conn.commit()
        print(f"Processed {len(unprocessed)} images")

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    process_images()