"""
MCP Tool: Update Task

This module implements the update_task MCP tool that integrates with the
existing update_task_skill to modify tasks.
"""
from typing import Dict, Any
from pydantic import BaseModel
from typing import Optional, List
from backend.mcp.models import MCPTaskPriority

class UpdateTaskParams(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[MCPTaskPriority] = None
    due_date: Optional[str] = None
    completed: Optional[bool] = None

def validate_update_task_params(params: UpdateTaskParams) -> dict:
    # Placeholder validation - replace with actual validation logic from .claude/skills
    is_valid = True
    errors = []
    if params.task_id is None:
        is_valid = False
        errors.append({"field": "task_id", "message": "Task ID cannot be empty"})
    return {"is_valid": is_valid, "errors": errors}


async def update_task_tool(user_id: int, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    MCP tool for updating an existing task in the user's todo list.

    Args:
        user_id: The ID of the user making the request
        params: Parameters for updating the task
        session_id: The session ID for the request

    Returns:
        Dict[str, Any]: Result of the operation
    """
    from mcp.integration import get_integration_manager
    from mcp.context import get_context_manager
    # Get the integration manager to access the skill adapter
    integration_manager = get_integration_manager()

    # Validate parameters
    try:
        # Check if task_id is provided
        if "task_id" not in params or not params["task_id"]:
            return {
                "success": False,
                "error": "validation_error",
                "message": "task_id is required for updating a task",
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }

        # Create UpdateTaskParams object for validation
        validation_params = UpdateTaskParams(**{
            k: v for k, v in params.items()
            if k in ["task_id", "title", "description", "priority", "due_date", "completed", "tags"]
        })

        validation_result = validate_update_task_params(validation_params)

        if not validation_result["is_valid"]:
            return {
                "success": False,
                "error": "validation_error",
                "message": "Invalid parameters provided",
                "details": validation_result["errors"],
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }
    except Exception as e:
        return {
            "success": False,
            "error": "validation_error",
            "message": f"Parameter validation failed: {str(e)}",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }

    # Execute the skill via MCP integration
    result = await integration_manager.execute_skill_via_mcp(
        skill_name="update_task",
        user_id=user_id,
        params=params,
        session_id=session_id
    )

    # Update context if successful
    if result.get("success"):
        task_id = params.get("task_id")
        if task_id:
            context_manager = get_context_manager()
            context_manager.reference_task(session_id, task_id)
            context_manager.set_last_task_action(session_id, "update", task_id)

    return result