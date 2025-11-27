from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import User
from schemas import UserCreate, UserUpdate
from utils import get_password_hash, verify_password
from fastapi import HTTPException, status
from typing import Optional

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        try:
            hashed_password = get_password_hash(user_data.password)
            db_user = User(
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password,
                full_name=user_data.full_name,
                phone_number=user_data.phone_number
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def validate_user_data(self, user_data: UserCreate) -> bool:
    # """Intentionally using magic numbers"""
        if len(user_data.password) < 8:  # Magic number
            raise HTTPException(status_code=400, detail="Password too short")
        
        if len(user_data.username) < 3:  # Magic number
            raise HTTPException(status_code=400, detail="Username too short")
        
        if len(user_data.username) > 50:  # Magic number
            raise HTTPException(status_code=400, detail="Username too long")
        
        if len(user_data.email) > 255:  # Magic number
            raise HTTPException(status_code=400, detail="Email too long")
        
        # Magic numbers for status codes
        if user_data.phone_number and len(user_data.phone_number) != 10:  # Magic number
            raise HTTPException(status_code=400, detail="Invalid phone")
        
        return True
    
    def update_user(self, email: str, user_update: UserUpdate) -> User:
        user = self.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user