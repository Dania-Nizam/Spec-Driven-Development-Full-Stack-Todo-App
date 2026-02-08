"""
Direct database implementations for MCP skills.
These functions directly interact with the database instead of making HTTP calls.
"""
from typing import Dict, Any, Optional, List
from sqlmodel import Session, select
from datetime import datetime
from backend.models.user import Task, TaskCreate, User
from database.session import engine


async def add_task_skill(
    user_id: int,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Add a new task directly to the database.

    Args:
        user_id: The ID of the user
        title: Task title
        description: Task description
        priority: Task priority (low, medium, high)
        due_date: Due date string
        tags: List of tags (not implemented in current schema)

    Returns:
        Dict with success status and task data
    """
    try:
        # Create database session directly
        with Session(engine) as session:
            # Create new task
            new_task = Task(
                title=title,
                description=description or "",
                completed=False,
                priority=priority.capitalize() if priority else "Medium",
                due_date=due_date,
                user_id=user_id
            )

            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            return {
                "success": True,
                "message": f"Task '{title}' added successfully",
                "task": {
                    "id": new_task.id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "completed": new_task.completed,
                    "priority": new_task.priority,
                    "due_date": new_task.due_date,
                    "user_id": new_task.user_id,
                    "created_at": new_task.created_at.isoformat(),
                    "updated_at": new_task.updated_at.isoformat()
                }
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to add task: {str(e)}"
        }


async def view_tasks_skill(
    user_id: int,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> Dict[str, Any]:
    """
    View tasks from the database.

    Args:
        user_id: The ID of the user
        status: Filter by completion status
        priority: Filter by priority
        limit: Maximum number of tasks to return
        offset: Number of tasks to skip
        sort_by: Field to sort by
        sort_order: Sort order (asc/desc)

    Returns:
        Dict with success status and tasks list
    """
    try:
        with Session(engine) as session:
            # Build query
            statement = select(Task).where(Task.user_id == user_id)

            # Apply filters
            if status and status.lower() != "all":
                if status.lower() == "completed":
                    statement = statement.where(Task.completed == True)
                elif status.lower() in ["pending", "incomplete"]:
                    statement = statement.where(Task.completed == False)

            if priority:
                statement = statement.where(Task.priority == priority.capitalize())

            # Apply sorting
            if sort_order.lower() == "desc":
                statement = statement.order_by(Task.created_at.desc())
            else:
                statement = statement.order_by(Task.created_at.asc())

            # Apply pagination
            if offset:
                statement = statement.offset(offset)
            if limit:
                statement = statement.limit(limit)

            # Execute query
            tasks = session.exec(statement).all()

            # Convert to dict
            tasks_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "user_id": task.user_id,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                for task in tasks
            ]

            return {
                "success": True,
                "message": f"Retrieved {len(tasks_list)} tasks",
                "tasks": tasks_list,
                "total_count": len(tasks_list),
                "filtered_count": len(tasks_list)
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to retrieve tasks: {str(e)}",
            "tasks": []
        }


async def update_task_skill(
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update a task in the database.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to update
        title: New title
        description: New description
        priority: New priority
        due_date: New due date
        completed: New completion status

    Returns:
        Dict with success status and updated task
    """
    try:
        with Session(engine) as session:
            # Get task
            task = session.get(Task, task_id)

            if not task or task.user_id != user_id:
                return {
                    "success": False,
                    "error": "Task not found or access denied",
                    "message": "Task not found"
                }

            # Update fields
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if priority is not None:
                task.priority = priority.capitalize()
            if due_date is not None:
                task.due_date = due_date
            if completed is not None:
                task.completed = completed

            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Task {task_id} updated successfully",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "user_id": task.user_id,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to update task: {str(e)}"
        }


async def delete_task_skill(
    user_id: int,
    task_id: int
) -> Dict[str, Any]:
    """
    Delete a task from the database.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task to delete

    Returns:
        Dict with success status
    """
    try:
        with Session(engine) as session:
            # Get task
            task = session.get(Task, task_id)

            if not task or task.user_id != user_id:
                return {
                    "success": False,
                    "error": "Task not found or access denied",
                    "message": "Task not found"
                }

            session.delete(task)
            session.commit()

            return {
                "success": True,
                "message": f"Task {task_id} deleted successfully"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to delete task: {str(e)}"
        }


async def mark_complete_skill(
    user_id: int,
    task_id: int,
    completed: bool = True
) -> Dict[str, Any]:
    """
    Mark a task as complete or incomplete.

    Args:
        user_id: The ID of the user
        task_id: The ID of the task
        completed: Whether to mark as complete (True) or incomplete (False)

    Returns:
        Dict with success status and updated task
    """
    return await update_task_skill(
        user_id=user_id,
        task_id=task_id,
        completed=completed
    )


async def search_filter_tasks_skill(
    user_id: int,
    query: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> Dict[str, Any]:
    """
    Search and filter tasks.

    Args:
        user_id: The ID of the user
        query: Search query for title/description
        status: Filter by status
        priority: Filter by priority
        tags: Filter by tags (not implemented)
        limit: Maximum results
        offset: Skip results
        sort_by: Sort field
        sort_order: Sort order

    Returns:
        Dict with success status and filtered tasks
    """
    try:
        with Session(engine) as session:
            # Build query
            statement = select(Task).where(Task.user_id == user_id)

            # Apply search query
            if query:
                statement = statement.where(
                    (Task.title.contains(query)) | (Task.description.contains(query))
                )

            # Apply filters (reuse view_tasks logic)
            if status and status.lower() != "all":
                if status.lower() == "completed":
                    statement = statement.where(Task.completed == True)
                elif status.lower() in ["pending", "incomplete"]:
                    statement = statement.where(Task.completed == False)

            if priority:
                statement = statement.where(Task.priority == priority.capitalize())

            # Apply sorting
            if sort_order.lower() == "desc":
                statement = statement.order_by(Task.created_at.desc())
            else:
                statement = statement.order_by(Task.created_at.asc())

            # Apply pagination
            if offset:
                statement = statement.offset(offset)
            if limit:
                statement = statement.limit(limit)

            # Execute
            tasks = session.exec(statement).all()

            tasks_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "user_id": task.user_id,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                for task in tasks
            ]

            return {
                "success": True,
                "message": f"Found {len(tasks_list)} matching tasks",
                "tasks": tasks_list,
                "filtered_count": len(tasks_list)
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to search tasks: {str(e)}",
            "tasks": []
        }


async def set_recurring_skill(
    user_id: int,
    task_id: int,
    frequency: str = "daily",
    ends_on: Optional[str] = None
) -> Dict[str, Any]:
    """
    Set a task as recurring (not fully implemented in current schema).

    Args:
        user_id: The ID of the user
        task_id: The ID of the task
        frequency: Recurrence frequency
        ends_on: End date for recurrence

    Returns:
        Dict with success status
    """
    return {
        "success": False,
        "error": "not_implemented",
        "message": "Recurring tasks are not yet implemented in the current schema"
    }


async def get_task_context_skill(
    user_id: int,
    task_ids: Optional[List[int]] = None,
    recent_count: int = 5,
    include_completed: bool = False
) -> Dict[str, Any]:
    """
    Get context about tasks (recent tasks or specific tasks).

    Args:
        user_id: The ID of the user
        task_ids: Specific task IDs to get context for
        recent_count: Number of recent tasks to return
        include_completed: Whether to include completed tasks

    Returns:
        Dict with success status and task context
    """
    try:
        with Session(engine) as session:
            if task_ids:
                # Get specific tasks
                statement = select(Task).where(
                    (Task.user_id == user_id) & (Task.id.in_(task_ids))
                )
            else:
                # Get recent tasks
                statement = select(Task).where(Task.user_id == user_id)

                if not include_completed:
                    statement = statement.where(Task.completed == False)

                statement = statement.order_by(Task.created_at.desc()).limit(recent_count)

            tasks = session.exec(statement).all()

            tasks_list = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                for task in tasks
            ]

            return {
                "success": True,
                "message": f"Retrieved context for {len(tasks_list)} tasks",
                "tasks": tasks_list,
                "task_count": len(tasks_list)
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to get task context: {str(e)}",
            "tasks": []
        }
