"""
Context management module for the MCP (Model Context Protocol) server.

This module handles conversation context for stateful interactions.
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from threading import Lock
import logging


logger = logging.getLogger(__name__)


class ConversationContextManager:
    """
    Manages conversation context for stateful interactions.
    """

    def __init__(self, context_ttl: int = 3600):  # 1 hour default TTL
        """
        Initialize the context manager.

        Args:
            context_ttl: Context time-to-live in seconds (default: 1 hour)
        """
        self.context_ttl = context_ttl
        self.contexts: Dict[str, Dict[str, Any]] = {}
        self.lock = Lock()  # Thread safety for context operations

    def create_context(self, session_id: str, user_id: int) -> str:
        """
        Create a new conversation context for a session.

        Args:
            session_id: The session ID
            user_id: The user ID

        Returns:
            str: The context ID
        """
        context_id = str(uuid.uuid4())
        now = datetime.utcnow()

        with self.lock:
            self.contexts[context_id] = {
                "context_id": context_id,
                "session_id": session_id,
                "user_id": user_id,
                "created_at": now,
                "last_updated_at": now,
                "expires_at": now + timedelta(seconds=self.context_ttl),
                "previous_tasks_referenced": [],
                "current_topic": "",
                "pending_clarifications": [],
                "conversation_history": [],
                "last_task_action": "",
                "last_task_id": None,
                "custom_data": {}
            }

        logger.info(f"Created new context {context_id} for session {session_id}")
        return context_id

    def get_context(self, session_id: str) -> Dict[str, Any]:
        """
        Get or create conversation context for a session.

        Args:
            session_id: The session ID

        Returns:
            Dict[str, Any]: The conversation context
        """
        # Find existing context for this session
        context = None
        with self.lock:
            for ctx_id, ctx_data in self.contexts.items():
                if ctx_data["session_id"] == session_id:
                    # Check if context has expired
                    if datetime.utcnow() > ctx_data["expires_at"]:
                        del self.contexts[ctx_id]
                        logger.info(f"Removed expired context {ctx_id}")
                    else:
                        context = ctx_data.copy()
                        break

        if context is None:
            # Create a new context if none exists
            logger.info(f"No existing context found for session {session_id}, creating new one")
            # We can't create a new context without user_id, so return a default one
            return {
                "context_id": "",
                "session_id": session_id,
                "user_id": None,
                "created_at": datetime.utcnow(),
                "last_updated_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(seconds=self.context_ttl),
                "previous_tasks_referenced": [],
                "current_topic": "",
                "pending_clarifications": [],
                "conversation_history": [],
                "last_task_action": "",
                "last_task_id": None,
                "custom_data": {}
            }

        return context

    def update_context(
        self,
        session_id: str,
        updates: Dict[str, Any],
        user_id: Optional[int] = None
    ) -> bool:
        """
        Update conversation context for a session.

        Args:
            session_id: The session ID
            updates: Dictionary of updates to apply to the context
            user_id: The user ID (for validation)

        Returns:
            bool: True if updated successfully, False otherwise
        """
        context_id = None
        with self.lock:
            # Find the context for this session
            for ctx_id, ctx_data in self.contexts.items():
                if ctx_data["session_id"] == session_id:
                    # Check if context has expired
                    if datetime.utcnow() > ctx_data["expires_at"]:
                        del self.contexts[ctx_id]
                        logger.info(f"Removed expired context {ctx_id}")
                    else:
                        context_id = ctx_id
                        break

            if context_id is None:
                # Create new context if none exists
                if user_id is not None:
                    context_id = self.create_context(session_id, user_id)
                else:
                    logger.warning(f"No context found for session {session_id} and no user_id provided")
                    return False

            if context_id in self.contexts:
                context = self.contexts[context_id]

                # Apply updates
                for key, value in updates.items():
                    if key in context:
                        if key == "previous_tasks_referenced" and isinstance(value, list):
                            # Extend the list instead of replacing
                            context[key].extend([tid for tid in value if tid not in context[key]])
                        elif key == "pending_clarifications" and isinstance(value, list):
                            # Extend the list instead of replacing
                            context[key].extend([item for item in value if item not in context[key]])
                        elif key == "conversation_history" and isinstance(value, list):
                            # Extend the list instead of replacing
                            context[key].extend(value)
                        elif key == "conversation_history" and isinstance(value, dict):
                            # Append a single turn to history
                            context[key].append(value)
                        else:
                            # Replace the value
                            context[key] = value

                # Update timestamps
                context["last_updated_at"] = datetime.utcnow()
                context["expires_at"] = datetime.utcnow() + timedelta(seconds=self.context_ttl)

                return True

        return False

    def add_conversation_turn(
        self,
        session_id: str,
        role: str,
        content: str,
        user_id: Optional[int] = None
    ) -> bool:
        """
        Add a conversation turn to the context.

        Args:
            session_id: The session ID
            role: The role of the speaker ("user" or "assistant")
            content: The content of the turn
            user_id: The user ID (for validation)

        Returns:
            bool: True if added successfully, False otherwise
        """
        turn = {
            "turn_id": str(uuid.uuid4()),
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }

        return self.update_context(session_id, {"conversation_history": turn}, user_id)

    def reference_task(self, session_id: str, task_id: int) -> bool:
        """
        Add a task to the list of referenced tasks in the context.

        Args:
            session_id: The session ID
            task_id: The task ID to reference

        Returns:
            bool: True if updated successfully, False otherwise
        """
        context = self.get_context(session_id)
        if task_id not in context.get("previous_tasks_referenced", []):
            return self.update_context(session_id, {"previous_tasks_referenced": [task_id]})
        return True

    def set_current_topic(self, session_id: str, topic: str) -> bool:
        """
        Set the current topic in the conversation context.

        Args:
            session_id: The session ID
            topic: The current topic

        Returns:
            bool: True if updated successfully, False otherwise
        """
        return self.update_context(session_id, {"current_topic": topic})

    def add_pending_clarification(self, session_id: str, clarification: str) -> bool:
        """
        Add a pending clarification to the context.

        Args:
            session_id: The session ID
            clarification: The clarification needed

        Returns:
            bool: True if added successfully, False otherwise
        """
        return self.update_context(session_id, {"pending_clarifications": [clarification]})

    def clear_pending_clarifications(self, session_id: str) -> bool:
        """
        Clear all pending clarifications from the context.

        Args:
            session_id: The session ID

        Returns:
            bool: True if cleared successfully, False otherwise
        """
        return self.update_context(session_id, {"pending_clarifications": []})

    def set_last_task_action(self, session_id: str, action: str, task_id: Optional[int] = None) -> bool:
        """
        Set the last task action in the context.

        Args:
            session_id: The session ID
            action: The action taken ("add", "update", "delete", "view", "mark_complete", "search", "set_recurring")
            task_id: The ID of the task affected (optional)

        Returns:
            bool: True if updated successfully, False otherwise
        """
        updates = {"last_task_action": action}
        if task_id is not None:
            updates["last_task_id"] = task_id

        return self.update_context(session_id, updates)

    def get_recent_tasks(self, session_id: str, count: int = 5) -> List[int]:
        """
        Get the most recently referenced tasks from the context.

        Args:
            session_id: The session ID
            count: Number of recent tasks to return (default: 5)

        Returns:
            List[int]: List of recent task IDs
        """
        context = self.get_context(session_id)
        return context.get("previous_tasks_referenced", [])[-count:]

    def cleanup_expired_contexts(self) -> int:
        """
        Clean up all expired contexts.

        Returns:
            int: Number of contexts cleaned up
        """
        expired_contexts = []
        now = datetime.utcnow()

        with self.lock:
            for context_id, context in self.contexts.items():
                if now > context["expires_at"]:
                    expired_contexts.append(context_id)

            for context_id in expired_contexts:
                del self.contexts[context_id]

        logger.info(f"Cleaned up {len(expired_contexts)} expired contexts")
        return len(expired_contexts)

    def get_context_size(self, session_id: str) -> int:
        """
        Get the approximate size of the context in characters.

        Args:
            session_id: The session ID

        Returns:
            int: Approximate size in characters
        """
        context = self.get_context(session_id)
        size = 0
        for key, value in context.items():
            if isinstance(value, str):
                size += len(value)
            elif isinstance(value, list):
                size += sum(len(str(item)) if not isinstance(item, dict) else len(str(item)) for item in value)
            elif isinstance(value, dict):
                size += len(str(value))
        return size

    def trim_context_history(self, session_id: str, max_turns: int = 20) -> bool:
        """
        Trim the conversation history to the most recent turns.

        Args:
            session_id: The session ID
            max_turns: Maximum number of turns to keep (default: 20)

        Returns:
            bool: True if trimmed successfully, False otherwise
        """
        context = self.get_context(session_id)
        history = context.get("conversation_history", [])

        if len(history) > max_turns:
            trimmed_history = history[-max_turns:]
            return self.update_context(session_id, {"conversation_history": trimmed_history})

        return True


class ContextValidator:
    """
    Validator for conversation context data.
    """

    @staticmethod
    def validate_context_updates(updates: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate context update data.

        Args:
            updates: Dictionary of updates to validate

        Returns:
            tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        # Validate task IDs are integers
        if "previous_tasks_referenced" in updates:
            if not isinstance(updates["previous_tasks_referenced"], list):
                return False, "previous_tasks_referenced must be a list"
            for task_id in updates["previous_tasks_referenced"]:
                if not isinstance(task_id, int) or task_id <= 0:
                    return False, f"All task IDs must be positive integers, got {task_id}"

        # Validate role in conversation history
        if "conversation_history" in updates:
            if isinstance(updates["conversation_history"], list):
                for turn in updates["conversation_history"]:
                    if not isinstance(turn, dict):
                        continue
                    if "role" in turn and turn["role"] not in ["user", "assistant"]:
                        return False, f"Role must be 'user' or 'assistant', got {turn['role']}"
            elif isinstance(updates["conversation_history"], dict):
                if updates["conversation_history"].get("role") not in ["user", "assistant"]:
                    return False, f"Role must be 'user' or 'assistant', got {updates['conversation_history'].get('role')}"

        # Validate last task action
        if "last_task_action" in updates:
            valid_actions = ["add", "update", "delete", "view", "mark_complete", "search", "set_recurring"]
            if updates["last_task_action"] not in valid_actions:
                return False, f"last_task_action must be one of {valid_actions}"

        return True, None


# Global context manager instance
context_manager = ConversationContextManager()


def get_context_manager() -> ConversationContextManager:
    """
    Get the global context manager instance.

    Returns:
        ConversationContextManager: The context manager instance
    """
    return context_manager