"""
Authentication dependencies for protected routes.
"""
from fastapi import Depends
from backend.api.deps import get_current_user


async def get_current_user_id(
    current_user: dict = Depends(get_current_user)
) -> int:
    """
    Extract user_id from the authenticated user.
    Used by chat and other protected endpoints.
    """
    return current_user["user_id"]
