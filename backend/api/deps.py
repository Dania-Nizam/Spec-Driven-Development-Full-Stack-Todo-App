from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/sign-in/email")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # settings.BETTER_AUTH_SECRET use karna zaroori hai
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
        return {"user_id": int(user_id)}
    except JWTError as e:
        print(f"Debug Error: {str(e)}") # Terminal mein expiry ya signature error dikhayega
        raise credentials_exception