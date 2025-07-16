from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String)
    message_text = Column(Text)
    date = Column(DateTime)
    views = Column(Integer)
    
class ProductMention(Base):
    __tablename__ = "product_mentions"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer)
    product_name = Column(String)
    context = Column(Text)
    is_medicine = Column(Boolean)
    
class ChannelActivity(Base):
    __tablename__ = "channel_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String)
    date = Column(DateTime)
    message_count = Column(Integer)
    total_views = Column(Integer)