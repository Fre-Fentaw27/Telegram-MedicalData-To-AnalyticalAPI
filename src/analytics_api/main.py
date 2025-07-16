from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import get_db, Base, engine
from models import Message, ProductMention, ChannelActivity
from schemas import (
    ProductMentionResponse,
    ChannelActivityResponse,
    MessageSearchResponse
)
from crud import (
    get_top_products,
    get_channel_activity,
    search_messages
)
from sqlalchemy.orm import Session

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/reports/top-products", response_model=List[ProductMentionResponse])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return get_top_products(db, limit)

@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivityResponse])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    activity = get_channel_activity(db, channel_name)
    if not activity:
        raise HTTPException(status_code=404, detail="Channel not found or no activity")
    return activity

@app.get("/api/search/messages", response_model=List[MessageSearchResponse])
def search_messages_endpoint(query: str, limit: int = 100, db: Session = Depends(get_db)):
    return search_messages(db, query, limit)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)