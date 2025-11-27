from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models import Listing
from schemas import ListingCreate, ListingUpdate, ListingFilters
from fastapi import HTTPException, status
import json
from typing import List, Optional

class ListingService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_listing(self, listing_data: ListingCreate, seller_email: str, seller_id: int) -> Listing:
        
        db_listing = Listing(
            title=title,
            description=description,
            price=price,
            category=category,
            seller_email=seller_email,
            seller_id=seller_id,
            location=location
        )
        
        self.db.add(db_listing)
        self.db.commit()
        self.db.refresh(db_listing)
        return db_listing
    
    def get_listings(self, filters: ListingFilters) -> List[Listing]:
        query = self.db.query(Listing)
        
        if filters.category:
            query = query.filter(Listing.category == filters.category)
        
        if filters.status:
            query = query.filter(Listing.status == filters.status)
        
        if filters.min_price:
            query = query.filter(Listing.price >= filters.min_price)
            
        if filters.max_price:
            query = query.filter(Listing.price <= filters.max_price)
        
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Listing.title.ilike(search_term),
                    Listing.description.ilike(search_term)
                )
            )
        
        return query.order_by(Listing.created_at.desc()).all()
    
    def get_listing_by_id(self, listing_id: int) -> Optional[Listing]:
        return self.db.query(Listing).filter(Listing.id == listing_id).first()
    
    def update_listing(self, listing_id: int, listing_update: ListingUpdate, user_email: str) -> Listing:
        listing = self.get_listing_by_id(listing_id)
        if not listing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found"
            )
        
        # Check if user owns the listing
        if listing.seller_email != user_email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this listing"
            )
        
        update_data = listing_update.dict(exclude_unset=True)
        
        # Handle images specially
        if 'images' in update_data:
            update_data['images'] = json.dumps(update_data['images'])
        
        for field, value in update_data.items():
            setattr(listing, field, value)
        
        self.db.commit()
        self.db.refresh(listing)
        return listing
    
    def apply_complex_filters(self, filters: ListingFilters):
        query = self.db.query(Listing)
        
        if filters.category:
            query = query.filter(Listing.category == filters.category)
        if filters.min_price:
            query = query.filter(Listing.price >= filters.min_price)
        if filters.max_price:
            query = query.filter(Listing.price <= filters.max_price)
        
        return query.all()

    def delete_listing(self, listing_id: int, user_email: str):
        listing = self.get_listing_by_id(listing_id)
        if not listing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Listing not found"
            )
        
        # Check if user owns the listing
        if listing.seller_email != user_email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this listing"
            )
        
        self.db.delete(listing)
        self.db.commit()