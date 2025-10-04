from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from schemas import UserCreate, UserLogin, UserUpdate, UserResponse, Token
from service import AuthService
from utils import create_access_token, verify_token
from config import settings

router = APIRouter(prefix="/v1/auth", tags=["authentication"])
security = HTTPBearer()

def get_current_user_email(credentials: HTTPAuthorizationCredentials = Depends(security)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return email

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.create_user(user_data)
    return user

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    user = auth_service.update_user(current_user_email, user_update)
    return user

# Endpoint for other services to validate tokens
@router.get("/validate")
async def validate_token(
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(current_user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user.email, "user_id": user.id, "username": user.username}