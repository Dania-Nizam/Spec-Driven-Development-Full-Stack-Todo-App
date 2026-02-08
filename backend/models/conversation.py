"""
Conversation and Message models for stateless chat with database persistence.
Implements Hackathon II specification for chat history storage.
"""
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.user import User


class Conversation(SQLModel, table=True):
    """
    Conversation model - represents a chat session between user and AI.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Message model - represents individual messages in a conversation.
    Stores both user messages and assistant responses.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(
        sa_column=Column(Integer, ForeignKey("conversation.id", ondelete="CASCADE"), index=True)
    )
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field()  # The actual message text
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls made
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
    user: Optional["User"] = Relationship(back_populates="messages")


# Pydantic schemas for API requests/responses
class ConversationCreate(SQLModel):
    """Schema for creating a new conversation"""
    pass  # No fields needed, user_id comes from auth


class ConversationRead(SQLModel):
    """Schema for reading conversation data"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class MessageCreate(SQLModel):
    """Schema for creating a new message"""
    conversation_id: Optional[int] = None
    message: str


class MessageRead(SQLModel):
    """Schema for reading message data"""
    id: int
    conversation_id: int
    user_id: int
    role: str
    content: str
    tool_calls: Optional[str] = None
    created_at: datetime
