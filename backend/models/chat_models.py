from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    conversation_context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    conversation_context: Dict[str, Any]
    success: bool = True
    error: Optional[str] = None
    timestamp: datetime = datetime.utcnow()
