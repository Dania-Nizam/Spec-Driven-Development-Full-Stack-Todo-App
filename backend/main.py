import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from database.session import engine
# Import all models so SQLModel.metadata knows about them
from backend.models import User, Task, Conversation, Message

# ---------------- APP INIT ----------------
app = FastAPI(title="Todo & Chat API", version="1.0.0")

@app.get("/")
def root():
    return {
        "message": "Backend chal raha hai! API docs ke liye jaao: http://localhost:8000/docs",
        "status": "ok",
        "routers_loaded": ["auth", "tasks"]  # chat load hone pe add kar dena
    }
# ---------------- DATABASE ----------------
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- ROUTERS ----------------

# ✅ Auth Router
try:
    from backend.api.auth import router as auth_router
    app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
    print("✅ Auth router loaded")
except ImportError as e:
    print(f"❌ Auth router not loaded: {e}")


# ✅ Tasks Router
try:
    from backend.api.tasks import router as tasks_router
    app.include_router(tasks_router, tags=["Tasks"])  # No prefix - routes already have full paths
    print("✅ Tasks router loaded")
except ImportError as e:
    print(f"❌ Tasks router not loaded: {e}")


## ✅ Chat Router
try:
    from backend.api.chat_new import router as chat_router
    app.include_router(chat_router)  # prefix chat.py me hai
    print("✅ Chat router loaded")
except ImportError as e:
    print(f"❌ Chat router error: {e}")

## ✅ Conversations Router
try:
    from backend.api.conversations import router as conversations_router
    app.include_router(conversations_router)
    print("✅ Conversations router loaded")
except ImportError as e:
    print(f"❌ Conversations router error: {e}")
# ---------------- ERROR HANDLER ----------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc.detail)},
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port="8000", reload=True)
