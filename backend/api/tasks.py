from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from models.user import Task, TaskCreate
from api.deps import get_current_user
from database.session import get_session

router = APIRouter()

# 1. Sare Tasks dikhane ke liye
@router.get("/api/{user_id}/tasks", response_model=List[Task])
async def list_tasks(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if int(current_user["user_id"]) != int(user_id):
        raise HTTPException(status_code=403, detail="User ID mismatch")
    
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()

# 2. Naya Task add karne ke liye
@router.post("/api/{user_id}/tasks", response_model=Task)
async def create_task(
    user_id: int,
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if int(current_user["user_id"]) != int(user_id):
        raise HTTPException(status_code=403, detail="User ID mismatch")
    
    new_task = Task(
        title=task_data.title,
        description=task_data.description or "",
        completed=False,
        user_id=user_id
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

# 3. DELETE OPTION: Task khatam karne ke liye
@router.delete("/api/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: int,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if int(current_user["user_id"]) != int(user_id):
        raise HTTPException(status_code=403, detail="User ID mismatch")
    
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
        
    session.delete(task)
    session.commit()
    return {"message": "Deleted"}

# 4. TOGGLE OPTION: Check/Uncheck logic handle karega
@router.patch("/api/{user_id}/tasks/{task_id}/toggle")
async def toggle_task(
    user_id: int, 
    task_id: int, 
    current_user: dict = Depends(get_current_user), 
    session: Session = Depends(get_session)
):
    # Check karein ke task isi user ka hai
    if int(current_user["user_id"]) != int(user_id):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Task ko database se dhoondein
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Status ulat dein (True hai toh False, False hai toh True)
    task.completed = not task.completed
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task