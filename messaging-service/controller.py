from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from schemas import ConversationCreate, ConversationResponse, MessageCreate, MessageResponse
from service import MessagingService
from external_clients import AuthClient, ListingsClient
from typing import List

router = APIRouter(prefix="/v1/conversations", tags=["messaging"])
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_info = await AuthClient.validate_token(credentials.credentials)
    return user_info

@router.get("/", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messaging_service = MessagingService(db)
    conversations = messaging_service.get_user_conversations(current_user["user_id"])
    return conversations

@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get listing information from listings service
    listing_info = await ListingsClient.get_listing(conversation_data.listing_id)
    
    messaging_service = MessagingService(db)
    conversation = messaging_service.create_conversation(conversation_data, current_user, listing_info)
    return conversation

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messaging_service = MessagingService(db)
    messages = messaging_service.get_conversation_messages(conversation_id, current_user["user_id"])
    return messages

@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messaging_service = MessagingService(db)
    message = messaging_service.create_message(conversation_id, message_data, current_user)
    return message
