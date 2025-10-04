from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from schemas import ListingCreate, ListingUpdate, ListingResponse, ListingFilters
from models import ListingCategory, ListingStatus
from service import ListingService
from auth_client import AuthClient
import json
from typing import List, Optional

router = APIRouter(prefix="/v1/listings", tags=["listings"])
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_info = await AuthClient.validate_token(credentials.credentials)
    return user_info

def parse_images(listing):
    """Parse images JSON string to list"""
    if listing.images:
        try:
            listing.images = json.loads(listing.images)
        except json.JSONDecodeError:
            listing.images = []
    else:
        listing.images = []
    return listing

@router.get("/", response_model=List[ListingResponse])
async def get_listings(
    category: Optional[ListingCategory] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    status: Optional[ListingStatus] = ListingStatus.AVAILABLE,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    filters = ListingFilters(
        category=category,
        min_price=min_price,
        max_price=max_price,
        status=status,
        search=search
    )
    
    listing_service = ListingService(db)
    listings = listing_service.get_listings(filters)
    
    # Parse images for each listing
    parsed_listings = [parse_images(listing) for listing in listings]
    return parsed_listings

@router.post("/", response_model=ListingResponse)
async def create_listing(
    listing_data: ListingCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    listing_service = ListingService(db)
    listing = listing_service.create_listing(
        listing_data, 
        current_user["email"], 
        current_user["user_id"]
    )
    return parse_images(listing)

@router.get("/{listing_id}", response_model=ListingResponse)
async def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing_service = ListingService(db)
    listing = listing_service.get_listing_by_id(listing_id)
    
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    return parse_images(listing)

@router.patch("/{listing_id}", response_model=ListingResponse)
async def update_listing(
    listing_id: int,
    listing_update: ListingUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    listing_service = ListingService(db)
    listing = listing_service.update_listing(listing_id, listing_update, current_user["email"])
    return parse_images(listing)

@router.delete("/{listing_id}")
async def delete_listing(
    listing_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    listing_service = ListingService(db)
    listing_service.delete_listing(listing_id, current_user["email"])
    return {"message": "Listing deleted successfully"}