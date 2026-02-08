"""
Authentication module for the MCP (Model Context Protocol) server.

This module provides JWT token verification and user authentication
for MCP tool calls.
"""
from typing import Optional, Tuple, Dict, Any
from jose import JWTError, jwt
from datetime import datetime
import os
from fastapi import HTTPException, status
import logging


logger = logging.getLogger(__name__)


def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and extract user information.

    Args:
        token: The JWT token to verify

    Returns:
        Optional[Dict[str, Any]]: User information if token is valid, None otherwise
    """
    # Get secret key from environment
    secret_key = os.getenv("BETTER_AUTH_SECRET")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    if not secret_key:
        raise ValueError("BETTER_AUTH_SECRET environment variable must be set")

    try:
        # Decode the token
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])

        # Extract user information
        user_id = payload.get("user_id")
        email = payload.get("email")
        exp = payload.get("exp")

        if user_id is None:
            logger.warning("Token missing user_id claim")
            return None

        # Check if token is expired
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            logger.warning("Token is expired")
            return None

        # Return user information
        return {
            "user_id": user_id,
            "email": email,
            "exp": exp
        }

    except JWTError as e:
        logger.warning(f"JWT verification failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during JWT verification: {str(e)}")
        return None


def authenticate_mcp_request(authorization_header: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate an MCP request using the Authorization header.

    Args:
        authorization_header: The Authorization header value (e.g., "Bearer <token>")

    Returns:
        Optional[Dict[str, Any]]: User information if authenticated, None otherwise
    """
    if not authorization_header:
        return None

    # Split the header to get the token
    parts = authorization_header.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning("Invalid Authorization header format")
        return None

    token = parts[1]
    return verify_jwt_token(token)


def validate_user_access(user_info: Dict[str, Any], requested_user_id: int) -> bool:
    """
    Validate that the authenticated user has access to the requested resource.

    Args:
        user_info: Information about the authenticated user
        requested_user_id: The user ID of the requested resource

    Returns:
        bool: True if access is granted, False otherwise
    """
    if not user_info:
        return False

    authenticated_user_id = user_info.get("user_id")
    return authenticated_user_id == requested_user_id


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user ID from a JWT token.

    Args:
        token: The JWT token

    Returns:
        Optional[int]: User ID if valid, None otherwise
    """
    user_info = verify_jwt_token(token)
    if user_info:
        return user_info.get("user_id")
    return None


def create_auth_error_response(error_code: str, message: str) -> Dict[str, Any]:
    """
    Create a standardized authentication error response.

    Args:
        error_code: The error code
        message: The error message

    Returns:
        Dict[str, Any]: The error response
    """
    return {
        "success": False,
        "error": error_code,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }


def handle_auth_error(error_code: str, message: str, status_code: int = 401) -> HTTPException:
    """
    Create an HTTP exception for authentication errors.

    Args:
        error_code: The error code
        message: The error message
        status_code: The HTTP status code (default: 401)

    Returns:
        HTTPException: The HTTP exception
    """
    error_response = create_auth_error_response(error_code, message)
    return HTTPException(
        status_code=status_code,
        detail=error_response
    )


def verify_mcp_tool_access(
    authorization_header: str,
    expected_user_id: int
) -> Tuple[Optional[Dict[str, Any]], Optional[HTTPException]]:
    """
    Verify MCP tool access by authenticating the request and validating user access.

    Args:
        authorization_header: The Authorization header value
        expected_user_id: The expected user ID for the operation

    Returns:
        Tuple[Optional[Dict[str, Any]], Optional[HTTPException]]:
            User information if valid, otherwise an HTTP exception
    """
    # Authenticate the request
    user_info = authenticate_mcp_request(authorization_header)

    if not user_info:
        return None, handle_auth_error(
            "unauthorized",
            "Invalid or missing JWT token",
            status.HTTP_401_UNAUTHORIZED
        )

    # Validate user access
    if not validate_user_access(user_info, expected_user_id):
        return None, handle_auth_error(
            "forbidden",
            "Access denied: User ID mismatch or insufficient permissions",
            status.HTTP_403_FORBIDDEN
        )

    # Check if token is about to expire (within 5 minutes)
    exp = user_info.get("exp")
    if exp:
        exp_datetime = datetime.fromtimestamp(exp)
        if exp_datetime < datetime.utcnow().replace(second=0, microsecond=0) + timedelta(minutes=5):
            logger.warning(f"Token for user {expected_user_id} is expiring soon")

    return user_info, None