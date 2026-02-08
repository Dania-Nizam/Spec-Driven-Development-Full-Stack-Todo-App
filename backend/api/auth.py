from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlmodel import Session, select
from database.session import get_session
from backend.models.user import User
from core.security import get_password_hash, create_access_token, verify_password
from .deps import get_current_user
from typing import Optional

router = APIRouter()

@router.post("/sign-up/email")
def signup(user_data: dict, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_data["email"])
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user_data["email"],
        hashed_password=get_password_hash(user_data["password"]),
        full_name=user_data.get("name", "")
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User created successfully"}

@router.post("/sign-in/email")
def login(data: dict, response: Response, session: Session = Depends(get_session)):
    # 1. User ko database mein find karein
    statement = select(User).where(User.email == data["email"])
    user = session.exec(statement).first()
    
    # 2. Password verify karein
    if not user or not verify_password(data["password"], user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # 3. Token generate karein
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    
    # 4. Cookie set karein (Next.js/Auth-client ke liye)
    # Note: 'access_token' key zyada standard hai, lekin agar aapki library 
    # 'session_token' mangti hai toh wahi rehne dein.
    response.set_cookie(
        key="access_token", 
        value=access_token,
        httponly=False,  # Frontend JS read kar sakay
        max_age=3600 * 24, # 24 hours
        samesite="lax",
        secure=False     # Localhost par False
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "name": user.full_name}
    }

@router.get("/get-session")
async def get_auth_session(request: Request):
    token = request.cookies.get("access_token") # Browser se token lega

    if token:
        try:
            # FIX: 'await' lagana zaroori hai
            user_info = await get_current_user(token)
            # Better Auth expects 'id' not 'user_id'
            return {
                "user": {
                    "id": user_info["user_id"],
                    "email": user_info.get("email"),
                    "name": user_info.get("name")
                },
                "session": {"active": True}
            }
        except:
            pass

    return {"user": None, "session": None}

@router.post("/sign-out")
async def sign_out(response: Response):
    """Sign out user by clearing the access_token cookie"""
    response.delete_cookie(key="access_token")
    return {"message": "Signed out successfully"}

    