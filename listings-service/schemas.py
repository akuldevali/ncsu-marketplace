from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models import ListingStatus, ListingCategory

class ListingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: ListingCategory
    location: Optional[str] = None
    images: Optional[List[str]] = []

class ListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[ListingCategory] = None
    status: Optional[ListingStatus] = None
    location: Optional[str] = None
    images: Optional[List[str]] = None

class ListingResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    category: ListingCategory
    status: ListingStatus
    seller_email: str
    seller_id: int
    location: Optional[str]
    images: List[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ListingFilters(BaseModel):
    category: Optional[ListingCategory] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    status: Optional[ListingStatus] = ListingStatus.AVAILABLE
    search: Optional[str] = None