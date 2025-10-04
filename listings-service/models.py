from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from database import Base
import enum

class ListingStatus(enum.Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    PENDING = "pending"

class ListingCategory(enum.Enum):
    TEXTBOOKS = "textbooks"
    ELECTRONICS = "electronics"
    FURNITURE = "furniture"
    CLOTHING = "clothing"
    SPORTS = "sports"
    OTHER = "other"

class Listing(Base):
    __tablename__ = "listings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(SQLEnum(ListingCategory), nullable=False)
    status = Column(SQLEnum(ListingStatus), default=ListingStatus.AVAILABLE)
    seller_email = Column(String, nullable=False)
    seller_id = Column(Integer, nullable=False)
    location = Column(String)
    images = Column(Text)  # JSON string of image URLs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())