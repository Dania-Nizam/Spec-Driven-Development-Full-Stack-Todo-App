"""
Conversation API routes for managing chat history.
Provides endpoints for retrieving and managing conversations.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime

from backend.models.conversation import ConversationRead, MessageRead
from backend.api.dependencies.auth import get_current_user_id
from backend.mcp.conversation_manager import get_conversation_manager

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])


@router.get("/", response_model=List[ConversationRead])
async def list_conversations(
    authenticated_user_id: int = Depends(get_current_user_id),
    limit: Optional[int] = 20
):
    """
    Get all conversations for the authenticated user.

    Args:
        authenticated_user_id: The authenticated user ID
        limit: Maximum number of conversations to return

    Returns:
        List of conversations ordered by most recent
    """
    conv_manager = get_conversation_manager()
    conversations = conv_manager.get_user_conversations(
        user_id=authenticated_user_id,
        limit=limit
    )

    return [
        ConversationRead(
            id=conv.id,
            user_id=conv.user_id,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        )
        for conv in conversations
    ]


@router.get("/{conversation_id}/messages", response_model=List[MessageRead])
async def get_conversation_history(
    conversation_id: int,
    authenticated_user_id: int = Depends(get_current_user_id),
    limit: Optional[int] = 50
):
    """
    Get message history for a specific conversation.

    Args:
        conversation_id: The conversation ID
        authenticated_user_id: The authenticated user ID
        limit: Maximum number of messages to return

    Returns:
        List of messages ordered by creation time
    """
    conv_manager = get_conversation_manager()

    # Verify conversation belongs to user
    conversation = conv_manager.get_conversation(conversation_id, authenticated_user_id)
    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found or access denied"
        )

    messages = conv_manager.get_conversation_history(
        conversation_id=conversation_id,
        user_id=authenticated_user_id,
        limit=limit
    )

    return [
        MessageRead(
            id=msg.id,
            conversation_id=msg.conversation_id,
            user_id=msg.user_id,
            role=msg.role,
            content=msg.content,
            tool_calls=msg.tool_calls,
            created_at=msg.created_at
        )
        for msg in messages
    ]


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    authenticated_user_id: int = Depends(get_current_user_id)
):
    """
    Delete a conversation and all its messages.

    Args:
        conversation_id: The conversation ID
        authenticated_user_id: The authenticated user ID

    Returns:
        Success message
    """
    conv_manager = get_conversation_manager()

    success = conv_manager.delete_conversation(
        conversation_id=conversation_id,
        user_id=authenticated_user_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found or access denied"
        )

    return {
        "success": True,
        "message": f"Conversation {conversation_id} deleted successfully",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/{conversation_id}", response_model=ConversationRead)
async def get_conversation(
    conversation_id: int,
    authenticated_user_id: int = Depends(get_current_user_id)
):
    """
    Get details of a specific conversation.

    Args:
        conversation_id: The conversation ID
        authenticated_user_id: The authenticated user ID

    Returns:
        Conversation details
    """
    conv_manager = get_conversation_manager()

    conversation = conv_manager.get_conversation(conversation_id, authenticated_user_id)
    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found or access denied"
        )

    return ConversationRead(
        id=conversation.id,
        user_id=conversation.user_id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )
