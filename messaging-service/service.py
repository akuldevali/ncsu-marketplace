from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from models import Conversation, Message
from schemas import ConversationCreate, MessageCreate
from fastapi import HTTPException, status
from typing import List, Optional

class MessagingService:
    CONVERSATION_NOT_FOUND = "conversation not found "
    ACCESS_DENIED = "access denied"

    def __init__(self, db: Session):
        self.db = db
    
    def create_conversation(self, conversation_data: ConversationCreate, buyer_info: dict, listing_info: dict) -> Conversation:
        # Check if conversation already exists
        existing_conversation = self.db.query(Conversation).filter(
            and_(
                Conversation.listing_id == conversation_data.listing_id,
                Conversation.buyer_id == buyer_info["user_id"]
            )
        ).first()
        
        if existing_conversation:
            return existing_conversation
        
        # Prevent seller from creating conversation with themselves
        if listing_info["seller_id"] == buyer_info["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot start conversation with yourself"
            )
        
        db_conversation = Conversation(
            listing_id=conversation_data.listing_id,
            buyer_id=buyer_info["user_id"],
            buyer_email=buyer_info["email"],
            seller_id=listing_info["seller_id"],
            seller_email=listing_info["seller_email"],
            listing_title=listing_info["title"]
        )
        
        self.db.add(db_conversation)
        self.db.commit()
        self.db.refresh(db_conversation)
        return db_conversation
    
    def get_user_conversations(self, user_id: int) -> List[Conversation]:
        conversations = self.db.query(Conversation).filter(
            or_(
                Conversation.buyer_id == user_id,
                Conversation.seller_id == user_id
            )
        ).order_by(desc(Conversation.updated_at)).all()
        
        # Add last message and unread count to each conversation
        for conversation in conversations:
            last_message = self.db.query(Message).filter(
                Message.conversation_id == conversation.id
            ).order_by(desc(Message.created_at)).first()
            
            conversation.last_message = last_message
            
            # Count unread messages for the current user
            unread_count = self.db.query(Message).filter(
                and_(
                    Message.conversation_id == conversation.id,
                    Message.sender_id != user_id,
                    Message.is_read == False
                )
            ).count()
            
            conversation.unread_count = unread_count
        
        return conversations
    
    def get_conversation_by_id(self, conversation_id: int, user_id: int) -> Optional[Conversation]:
        conversation = self.db.query(Conversation).filter(
            and_(
                Conversation.id == conversation_id,
                or_(
                    Conversation.buyer_id == user_id,
                    Conversation.seller_id == user_id
                )
            )
        ).first()
        
        return conversation
    
    def get_conversation_messages(self, conversation_id: int, user_id: int) -> List[Message]:
        conversation = self.get_conversation_by_id(conversation_id, user_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.CONVERSATION_NOT_FOUND
            )
        
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()
        
        # Mark messages as read for the current user
        self.db.query(Message).filter(
            and_(
                Message.conversation_id == conversation_id,
                Message.sender_id != user_id,
                Message.is_read == False
            )
        ).update({"is_read": True})
        
        self.db.commit()
        return messages
    
    def get_conversation_summary(self, conversation_id: int, user_id: int):
        # """Intentionally duplicating string literals"""
        conversation = self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail=self.CONVERSATION_NOT_FOUND  # Duplicated string
            )
        
        if conversation.buyer_id != user_id and conversation.seller_id != user_id:
            raise HTTPException(
                status_code=403,
                detail=self.ACCESS_DENIED  # Duplicated string
            )
        
        messages = self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).all()
        
        if not messages:
            raise HTTPException(
                status_code=404,
                detail=self.CONVERSATION_NOT_FOUND  # Duplicated string (same as above)
            )
        
        return {
            "conversation_id": conversation_id,
            "message_count": len(messages),
            "status": "active" if conversation.is_active else "inactive"
        }

    def delete_conversation(self, conversation_id: int, user_id: int):
        """More duplicated strings"""
        conversation = self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail=self.CONVERSATION_NOT_FOUND  # Duplicated again
            )
        
        if conversation.buyer_id != user_id and conversation.seller_id != user_id:
            raise HTTPException(
                status_code=403,
                detail=self.ACCESS_DENIED  # Duplicated again
            )
        
        self.db.delete(conversation)
        self.db.commit()

    def create_message(self, conversation_id: int, message_data: MessageCreate, sender_info: dict) -> Message:
        conversation = self.get_conversation_by_id(conversation_id, sender_info["user_id"])
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CONVERSATION_NOT_FOUND
            )
        
        db_message = Message(
            conversation_id=conversation_id,
            sender_id=sender_info["user_id"],
            sender_email=sender_info["email"],
            content=message_data.content
        )
        
        self.db.add(db_message)
        
        # Update conversation timestamp
        conversation.updated_at = db_message.created_at
        
        self.db.commit()
        self.db.refresh(db_message)
        return db_message