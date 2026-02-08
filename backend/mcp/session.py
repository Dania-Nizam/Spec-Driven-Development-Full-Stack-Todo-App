"""
Session management module for the MCP (Model Context Protocol) server.

This module handles MCP session creation, validation, and management.
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from threading import Lock
import logging


logger = logging.getLogger(__name__)


class SessionManager:
    """
    Manages MCP sessions for stateful conversation handling.
    """

    def __init__(self, session_timeout: int = 1800):
        """
        Initialize the session manager.

        Args:
            session_timeout: Session timeout in seconds (default: 30 minutes)
        """
        self.session_timeout = session_timeout
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.lock = Lock()  # Thread safety for session operations

    def create_session(self, user_id: int) -> str:
        """
        Create a new MCP session for a user.

        Args:
            user_id: The ID of the user

        Returns:
            str: The session ID
        """
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()

        with self.lock:
            self.sessions[session_id] = {
                "session_id": session_id,
                "user_id": user_id,
                "created_at": now,
                "last_activity_at": now,
                "expires_at": now + timedelta(seconds=self.session_timeout),
                "is_active": True,
                "tool_call_count": 0
            }

        logger.info(f"Created new session {session_id} for user {user_id}")
        return session_id

    def validate_session(self, session_id: str, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Validate an existing session for a user.

        Args:
            session_id: The session ID to validate
            user_id: The user ID associated with the session

        Returns:
            Optional[Dict[str, Any]]: Session information if valid, None otherwise
        """
        with self.lock:
            if session_id not in self.sessions:
                logger.warning(f"Session {session_id} not found")
                return None

            session = self.sessions[session_id]

            # Check if session belongs to the user
            if session["user_id"] != user_id:
                logger.warning(f"Session {session_id} does not belong to user {user_id}")
                return None

            # Check if session is active
            if not session["is_active"]:
                logger.warning(f"Session {session_id} is not active")
                return None

            # Check if session has expired
            if datetime.utcnow() > session["expires_at"]:
                self._expire_session(session_id)
                logger.warning(f"Session {session_id} has expired")
                return None

            return session.copy()

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session information without validation.

        Args:
            session_id: The session ID to retrieve

        Returns:
            Optional[Dict[str, Any]]: Session information if exists, None otherwise
        """
        with self.lock:
            if session_id in self.sessions:
                # Check if session has expired
                session = self.sessions[session_id]
                if datetime.utcnow() > session["expires_at"]:
                    self._expire_session(session_id)
                    return None
                return session.copy()
            return None

    def update_session_activity(self, session_id: str) -> bool:
        """
        Update the last activity time for a session.

        Args:
            session_id: The session ID to update

        Returns:
            bool: True if updated successfully, False otherwise
        """
        with self.lock:
            if session_id not in self.sessions:
                return False

            session = self.sessions[session_id]

            # Check if session has expired
            if datetime.utcnow() > session["expires_at"]:
                self._expire_session(session_id)
                return False

            # Update last activity time
            session["last_activity_at"] = datetime.utcnow()
            session["expires_at"] = datetime.utcnow() + timedelta(seconds=self.session_timeout)

            # Increment tool call counter
            session["tool_call_count"] = session.get("tool_call_count", 0) + 1

            return True

    def end_session(self, session_id: str) -> bool:
        """
        End a session (deactivate it).

        Args:
            session_id: The session ID to end

        Returns:
            bool: True if ended successfully, False otherwise
        """
        with self.lock:
            if session_id not in self.sessions:
                return False

            session = self.sessions[session_id]
            session["is_active"] = False
            logger.info(f"Ended session {session_id} for user {session['user_id']}")
            return True

    def cleanup_expired_sessions(self) -> int:
        """
        Clean up all expired sessions.

        Returns:
            int: Number of sessions cleaned up
        """
        expired_sessions = []
        now = datetime.utcnow()

        with self.lock:
            for session_id, session in self.sessions.items():
                if now > session["expires_at"]:
                    expired_sessions.append(session_id)

            for session_id in expired_sessions:
                self._expire_session(session_id)

        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        return len(expired_sessions)

    def get_active_sessions_count(self) -> int:
        """
        Get the count of active sessions.

        Returns:
            int: Number of active sessions
        """
        count = 0
        now = datetime.utcnow()

        with self.lock:
            for session in self.sessions.values():
                if session["is_active"] and now <= session["expires_at"]:
                    count += 1

        return count

    def _expire_session(self, session_id: str) -> None:
        """
        Internal method to expire a session.

        Args:
            session_id: The session ID to expire
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Expired session {session_id}")

    def get_user_sessions(self, user_id: int) -> list:
        """
        Get all sessions for a specific user.

        Args:
            user_id: The user ID

        Returns:
            list: List of session information for the user
        """
        user_sessions = []
        now = datetime.utcnow()

        with self.lock:
            for session in self.sessions.values():
                if session["user_id"] == user_id:
                    # Check if session is still valid
                    if now <= session["expires_at"]:
                        user_sessions.append(session.copy())
                    else:
                        self._expire_session(session["session_id"])

        return user_sessions

    def cleanup_user_sessions(self, user_id: int) -> int:
        """
        Clean up all sessions for a specific user.

        Args:
            user_id: The user ID

        Returns:
            int: Number of sessions cleaned up
        """
        sessions_to_remove = []

        with self.lock:
            for session_id, session in self.sessions.items():
                if session["user_id"] == user_id:
                    sessions_to_remove.append(session_id)

            for session_id in sessions_to_remove:
                del self.sessions[session_id]

        logger.info(f"Cleaned up {len(sessions_to_remove)} sessions for user {user_id}")
        return len(sessions_to_remove)


class MCPSessionHealthChecker:
    """
    Utility class for checking MCP session health.
    """

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    def get_health_report(self) -> Dict[str, Any]:
        """
        Get a health report for MCP sessions.

        Returns:
            Dict[str, Any]: Health report with session statistics
        """
        active_sessions = self.session_manager.get_active_sessions_count()
        total_sessions = len(self.session_manager.sessions)
        expired_sessions_removed = self.session_manager.cleanup_expired_sessions()

        return {
            "active_sessions": active_sessions,
            "total_sessions": total_sessions,
            "expired_sessions_cleaned": expired_sessions_removed,
            "timestamp": datetime.utcnow().isoformat()
        }


# Global session manager instance
session_manager = SessionManager()


def get_session_manager() -> SessionManager:
    """
    Get the global session manager instance.

    Returns:
        SessionManager: The session manager instance
    """
    return session_manager