from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

# 1. User Base Schema
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = Field(default=None)

# 2. Main User Table Model
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field() 
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tasks: List["Task"] = Relationship(back_populates="user")

# 3. Main Task Table Model
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="tasks")

# 4. Schemas
class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

# 5. Task related schemas
class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskRead(SQLModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None