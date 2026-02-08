"""
Conversation Manager for Database Persistence
Handles stateless chat with database persistence as required by Hackathon II specification.
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlmodel import Session, select

from backend.models.conversation import Conversation, Message, ConversationCreate, MessageCreate
from backend.database.session import engine

logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Manages conversation persistence to database.
    Implements stateless architecture - all state stored in DB.
    """

    def __init__(self):
        """Initialize the conversation manager."""
        pass

    def create_conversation(self, user_id: int, thread_id: Optional[str] = None) -> Conversation:
        """
        Create a new conversation in the database.

        Args:
            user_id: The authenticated user ID
            thread_id: Optional OpenAI thread ID for linking

        Returns:
            Created Conversation object
        """
        try:
            with Session(engine) as session:
                conversation = Conversation(
                    user_id=user_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(conversation)
                session.commit()
                session.refresh(conversation)

                logger.info(f"Created conversation {conversation.id} for user {user_id}")
                return conversation

        except Exception as e:
            logger.error(f"Error creating conversation: {str(e)}")
            raise

    def get_conversation(self, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """
        Get a conversation by ID, ensuring it belongs to the user.

        Args:
            conversation_id: The conversation ID
            user_id: The authenticated user ID

        Returns:
            Conversation object or None if not found
        """
        try:
            with Session(engine) as session:
                statement = select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
                conversation = session.exec(statement).first()
                return conversation

        except Exception as e:
            logger.error(f"Error getting conversation: {str(e)}")
            return None

    def get_or_create_conversation(
        self,
        user_id: int,
        conversation_id: Optional[int] = None
    ) -> Conversation:
        """
        Get existing conversation or create a new one.

        Args:
            user_id: The authenticated user ID
            conversation_id: Optional conversation ID to retrieve

        Returns:
            Conversation object
        """
        if conversation_id:
            conversation = self.get_conversation(conversation_id, user_id)
            if conversation:
                return conversation

        # Create new conversation if not found
        return self.create_conversation(user_id)

    def save_message(
        self,
        conversation_id: int,
        user_id: int,
        role: str,
        content: str,
        tool_calls: Optional[str] = None
    ) -> Message:
        """
        Save a message to the database.

        Args:
            conversation_id: The conversation ID
            user_id: The user ID
            role: Message role ("user" or "assistant")
            content: Message content
            tool_calls: Optional JSON string of tool calls made

        Returns:
            Created Message object
        """
        try:
            with Session(engine) as session:
                message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role=role,
                    content=content,
                    tool_calls=tool_calls,
                    created_at=datetime.utcnow()
                )
                session.add(message)
                session.commit()
                session.refresh(message)

                # Update conversation's updated_at timestamp
                conversation = session.get(Conversation, conversation_id)
                if conversation:
                    conversation.updated_at = datetime.utcnow()
                    session.add(conversation)
                    session.commit()

                logger.info(f"Saved {role} message to conversation {conversation_id}")
                return message

        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")
            raise

    def get_conversation_history(
        self,
        conversation_id: int,
        user_id: int,
        limit: Optional[int] = 50
    ) -> List[Message]:
        """
        Get conversation history from database.

        Args:
            conversation_id: The conversation ID
            user_id: The user ID (for security)
            limit: Maximum number of messages to retrieve

        Returns:
            List of Message objects ordered by creation time
        """
        try:
            with Session(engine) as session:
                # First verify the conversation belongs to the user
                conversation = session.get(Conversation, conversation_id)
                if not conversation or conversation.user_id != user_id:
                    logger.warning(f"Unauthorized access attempt to conversation {conversation_id}")
                    return []

                # Get messages
                statement = select(Message).where(
                    Message.conversation_id == conversation_id
                ).order_by(Message.created_at)

                if limit:
                    statement = statement.limit(limit)

                messages = session.exec(statement).all()
                return list(messages)

        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []

    def get_user_conversations(
        self,
        user_id: int,
        limit: Optional[int] = 20
    ) -> List[Conversation]:
        """
        Get all conversations for a user.

        Args:
            user_id: The user ID
            limit: Maximum number of conversations to retrieve

        Returns:
            List of Conversation objects ordered by updated_at (most recent first)
        """
        try:
            with Session(engine) as session:
                statement = select(Conversation).where(
                    Conversation.user_id == user_id
                ).order_by(Conversation.updated_at.desc())

                if limit:
                    statement = statement.limit(limit)

                conversations = session.exec(statement).all()
                return list(conversations)

        except Exception as e:
            logger.error(f"Error getting user conversations: {str(e)}")
            return []

    def delete_conversation(self, conversation_id: int, user_id: int) -> bool:
        """
        Delete a conversation and all its messages.

        Args:
            conversation_id: The conversation ID
            user_id: The user ID (for security)

        Returns:
            True if deleted, False otherwise
        """
        try:
            with Session(engine) as session:
                # Verify ownership
                conversation = session.get(Conversation, conversation_id)
                if not conversation or conversation.user_id != user_id:
                    logger.warning(f"Unauthorized delete attempt for conversation {conversation_id}")
                    return False

                # Delete conversation (messages will cascade delete due to relationship)
                session.delete(conversation)
                session.commit()

                logger.info(f"Deleted conversation {conversation_id}")
                return True

        except Exception as e:
            logger.error(f"Error deleting conversation: {str(e)}")
            return False

    def format_history_for_context(
        self,
        messages: List[Message],
        max_messages: Optional[int] = 10
    ) -> str:
        """
        Format conversation history as context string.

        Args:
            messages: List of Message objects
            max_messages: Maximum number of recent messages to include

        Returns:
            Formatted context string
        """
        if not messages:
            return ""

        # Take only the most recent messages
        recent_messages = messages[-max_messages:] if max_messages else messages

        context_lines = []
        for msg in recent_messages:
            role_label = "User" if msg.role == "user" else "Assistant"
            context_lines.append(f"{role_label}: {msg.content}")

        return "\n".join(context_lines)


# Global conversation manager instance
conversation_manager = ConversationManager()


def get_conversation_manager() -> ConversationManager:
    """
    Get the global conversation manager instance.

    Returns:
        ConversationManager instance
    """
    return conversation_manager
