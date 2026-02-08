from fastapi import Depends, HTTPException, status, Cookie, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import settings
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/sign-in/email", auto_error=False)

async def get_current_user(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    access_token: Optional[str] = Cookie(None)
):
    """
    Get current user from JWT token.
    Supports both Authorization header and Cookie-based authentication.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Try to get token from Authorization header first, then from cookie
    jwt_token = token or access_token

    if not jwt_token:
        print("Debug Error: No token found in Authorization header or cookie")
        raise credentials_exception

    try:
        # Using settings.BETTER_AUTH_SECRET is necessary
        payload = jwt.decode(jwt_token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise credentials_exception

        return {
            "user_id": int(user_id),
            "email": email
        }
    except JWTError as e:
        print(f"Debug Error: {str(e)}") # Terminal will show expiry or signature error
        raise credentials_exception