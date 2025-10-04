from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    sender_email: str
    content: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationCreate(BaseModel):
    listing_id: int

class ConversationResponse(BaseModel):
    id: int
    listing_id: int
    buyer_id: int
    buyer_email: str
    seller_id: int
    seller_email: str
    listing_title: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_message: Optional[MessageResponse] = None
    unread_count: int = 0
    
    class Config:
        from_attributes = True
