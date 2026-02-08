"""
MCP Tool: Add Task

This module implements the add_task MCP tool that integrates with the
existing add_task_skill to create new tasks.
"""
from typing import Dict, Any
from pydantic import BaseModel
from typing import Optional, List

class AddTaskParams(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[str] = None
    tags: Optional[List[str]] = []

def validate_add_task_params(params: AddTaskParams) -> dict:
    # Placeholder validation - replace with actual validation logic from .claude/skills
    is_valid = True
    errors = []
    if not params.title:
        is_valid = False
        errors.append({"field": "title", "message": "Title cannot be empty"})
    return {"is_valid": is_valid, "errors": errors}


async def add_task_tool(user_id: int, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    MCP tool for adding a new task to the user's todo list.

    Args:
        user_id: The ID of the user making the request
        params: Parameters for the task to add
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
        # Create AddTaskParams object for validation
        validation_params = AddTaskParams(**{
            k: v for k, v in params.items()
            if k in ["title", "description", "priority", "due_date", "tags"]
        })

        validation_result = validate_add_task_params(validation_params)

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
        skill_name="add_task",
        user_id=user_id,
        params=params,
        session_id=session_id
    )

    # Update context if successful
    if result.get("success"):
        task_id = result.get("result", {}).get("task", {}).get("id")
        if task_id:
            context_manager = get_context_manager()
            context_manager.reference_task(session_id, task_id)
            context_manager.set_last_task_action(session_id, "add", task_id)

    return result