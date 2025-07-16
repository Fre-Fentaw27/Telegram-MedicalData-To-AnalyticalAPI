from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ProductMentionBase(BaseModel):
    product_name: str
    is_medicine: bool

class ProductMentionResponse(ProductMentionBase):
    mention_count: int
    
    class Config:
        orm_mode = True

class ChannelActivityBase(BaseModel):
    date: datetime
    message_count: int
    total_views: int

class ChannelActivityResponse(ChannelActivityBase):
    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    channel_name: str
    message_text: str
    date: datetime
    views: int

class MessageSearchResponse(MessageBase):
    class Config:
        orm_mode = True

# Response models for your endpoints
class HealthCheckResponse(BaseModel):
    status: str
    database_status: str
    version: str