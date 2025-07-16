from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from models import ProductMention, Message, ChannelActivity

def get_top_products(db: Session, limit: int = 10):
    return db.query(
        ProductMention.product_name,
        func.count(ProductMention.id).label("mention_count"),
        ProductMention.is_medicine
    ).group_by(
        ProductMention.product_name,
        ProductMention.is_medicine
    ).order_by(
        func.count(ProductMention.id).desc()
    ).limit(limit).all()

def get_channel_activity(db: Session, channel_name: str):
    return db.query(ChannelActivity).filter(
        ChannelActivity.channel_name == channel_name
    ).order_by(ChannelActivity.date).all()

def search_messages(db: Session, query: str, limit: int = 100):
    return db.query(Message).filter(
        Message.message_text.ilike(f"%{query}%")
    ).order_by(Message.views.desc()).limit(limit).all()