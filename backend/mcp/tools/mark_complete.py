"""
MCP Tool: Mark Complete

This module implements the mark_complete MCP tool that integrates with the
existing mark_complete_skill to update task completion status.
"""
from typing import Dict, Any
from pydantic import BaseModel
from typing import Optional

class MarkCompleteParams(BaseModel):
    task_id: int
    completed: bool = True

def validate_mark_complete_params(params: MarkCompleteParams) -> dict:
    # Placeholder validation - replace with actual validation logic from .claude/skills
    is_valid = True
    errors = []
    if params.task_id is None:
        is_valid = False
        errors.append({"field": "task_id", "message": "Task ID cannot be empty"})
    return {"is_valid": is_valid, "errors": errors}


async def mark_complete_tool(user_id: int, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    MCP tool for marking a task as complete or incomplete.

    Args:
        user_id: The ID of the user making the request
        params: Parameters for marking the task complete
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
        # Check if task_id and completed are provided
        if "task_id" not in params or not params["task_id"]:
            return {
                "success": False,
                "error": "validation_error",
                "message": "task_id is required for marking a task complete",
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }

        if "completed" not in params:
            return {
                "success": False,
                "error": "validation_error",
                "message": "completed status is required for marking a task complete",
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }

        # Create MarkCompleteParams object for validation
        validation_params = MarkCompleteParams(**{
            k: v for k, v in params.items()
            if k in ["task_id", "completed"]
        })

        validation_result = validate_mark_complete_params(validation_params)

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
        skill_name="mark_complete",
        user_id=user_id,
        params=params,
        session_id=session_id
    )

    # Update context if successful
    if result.get("success"):
        task_id = params.get("task_id")
        completed = params.get("completed", True)
        if task_id:
            context_manager = get_context_manager()
            context_manager.reference_task(session_id, task_id)
            action = "mark_complete" if completed else "mark_incomplete"
            context_manager.set_last_task_action(session_id, action, task_id)

    return result