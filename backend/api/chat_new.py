"""
Chat API routes for the AI-powered todo chatbot.
Handles chat requests and orchestrates the conversation flow.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from datetime import datetime
import uuid
import logging

from backend.models.chat_models import ChatRequest, ChatResponse
from .dependencies.auth import get_current_user_id
from backend.mcp.mcp_sdk_adapter_simple import get_mcp_sdk_adapter
from backend.mcp.cohere_agent import CohereAgentOrchestrator
from backend.mcp.conversation_manager import get_conversation_manager
from backend.core.config import settings
import json

router = APIRouter(prefix="/api", tags=["Chat"])
logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    authenticated_user_id: int = Depends(get_current_user_id),
) -> ChatResponse:
    try:
        logger.info(f"Received chat message from user {authenticated_user_id}: {chat_request.message}")

        # Initialize conversation manager for DB persistence
        conv_manager = get_conversation_manager()

        # Get or create conversation in database (stateless architecture)
        conversation_id = None
        if chat_request.conversation_context:
            conversation_id = chat_request.conversation_context.get("conversation_id")

        conversation = conv_manager.get_or_create_conversation(
            user_id=authenticated_user_id,
            conversation_id=conversation_id
        )

        logger.info(f"Using conversation {conversation.id} for user {authenticated_user_id}")

        # Save user message to database
        user_message = conv_manager.save_message(
            conversation_id=conversation.id,
            user_id=authenticated_user_id,
            role="user",
            content=chat_request.message
        )

        # Get conversation history for Cohere (last 10 messages)
        messages = conv_manager.get_conversation_history(
            conversation_id=conversation.id,
            user_id=authenticated_user_id,
            limit=10
        )

        # Format history for Cohere (exclude the current message)
        chat_history = []
        for msg in messages[:-1]:  # Exclude the last message (current one)
            role = "USER" if msg.role == "user" else "CHATBOT"
            chat_history.append({"role": role, "message": msg.content})

        # Initialize Cohere Agent orchestrator with MCP SDK adapter
        logger.info("Initializing Cohere Agent with MCP tools...")
        mcp_adapter = get_mcp_sdk_adapter()
        orchestrator = CohereAgentOrchestrator(
            api_key=settings.COHERE_API_KEY,
            mcp_adapter=mcp_adapter
        )

        # Process the user's message using Cohere Agent
        logger.info("Processing message with Cohere Agent...")
        result = await orchestrator.process_message(
            user_id=authenticated_user_id,
            message=chat_request.message,
            conversation_history=chat_history
        )

        logger.info(f"Result: {result}")

        # Save assistant response to database
        assistant_message = conv_manager.save_message(
            conversation_id=conversation.id,
            user_id=authenticated_user_id,
            role="assistant",
            content=result.get("message", ""),
            tool_calls=None
        )

        # Build conversation context (stateless - all info from DB)
        conversation_context = {
            "conversation_id": conversation.id,
            "user_id": authenticated_user_id,
            "timestamp": datetime.utcnow().isoformat(),
        }

        response = ChatResponse(
            response=result.get("message", ""),
            session_id=str(conversation.id),
            conversation_context=conversation_context,
            success=result.get("success", True),
            error=result.get("error"),
            timestamp=datetime.utcnow(),
        )

        logger.info(f"Sending response: {response.response}")
        return response

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))