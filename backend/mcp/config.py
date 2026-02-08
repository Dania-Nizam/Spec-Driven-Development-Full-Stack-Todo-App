"""
Configuration module for the MCP (Model Context Protocol) server.

This module provides configuration settings and environment variable handling
for the MCP server.
"""
import os
from typing import Optional


class MCPConfig:
    """
    Configuration class for MCP server settings.
    """

    def __init__(self):
        # Server settings
        self.host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
        self.port = int(os.getenv("MCP_SERVER_PORT", "8001"))
        self.debug = os.getenv("MCP_SERVER_DEBUG", "false").lower() == "true"

        # Session settings
        self.session_timeout = int(os.getenv("MCP_SESSION_TIMEOUT", "1800"))  # 30 minutes in seconds
        self.max_concurrent_sessions = int(os.getenv("MCP_MAX_CONCURRENT_SESSIONS", "50"))

        # Logging settings
        self.log_level = os.getenv("MCP_LOG_LEVEL", "INFO")
        self.log_file = os.getenv("MCP_LOG_FILE", "logs/mcp-server.log")

        # Database settings (if needed for persistent sessions)
        self.database_url = os.getenv("DATABASE_URL", "")

        # Authentication settings
        self.jwt_secret = os.getenv("BETTER_AUTH_SECRET", "")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")

        # MCP-specific settings
        self.mcp_version = "1.0.0"
        self.max_tool_calls_per_minute = int(os.getenv("MCP_MAX_TOOL_CALLS_PER_MINUTE", "50"))
        self.max_context_size = int(os.getenv("MCP_MAX_CONTEXT_SIZE", "10000"))  # characters
        self.max_session_history = int(os.getenv("MCP_MAX_SESSION_HISTORY", "50"))  # turns

        # Validation
        self._validate_config()

    def _validate_config(self) -> None:
        """
        Validate the configuration settings.
        """
        if not self.jwt_secret:
            raise ValueError("BETTER_AUTH_SECRET environment variable must be set")

        if self.session_timeout <= 0:
            raise ValueError("MCP_SESSION_TIMEOUT must be a positive integer")

        if self.max_concurrent_sessions <= 0:
            raise ValueError("MCP_MAX_CONCURRENT_SESSIONS must be a positive integer")

    def get_database_url(self) -> Optional[str]:
        """
        Get the database URL if configured.

        Returns:
            Optional[str]: Database URL or None if not configured
        """
        return self.database_url if self.database_url else None

    def get_allowed_origins(self) -> list:
        """
        Get allowed origins for CORS.

        Returns:
            list: List of allowed origins
        """
        origins_str = os.getenv("MCP_ALLOWED_ORIGINS", "")
        if origins_str:
            return [origin.strip() for origin in origins_str.split(",")]
        else:
            # Default to allowing all in development, specific origins in production
            return ["*"] if self.debug else []


# Global configuration instance
mcp_config = MCPConfig()


def get_config() -> MCPConfig:
    """
    Get the global configuration instance.

    Returns:
        MCPConfig: The configuration instance
    """
    return mcp_config