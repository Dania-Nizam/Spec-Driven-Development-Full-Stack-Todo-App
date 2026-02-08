"""
MCP Tool: Set Recurring

This module implements the set_recurring MCP tool that integrates with the
existing set_recurring_skill to configure recurring tasks.
"""
from typing import Dict, Any
from pydantic import BaseModel
from typing import Optional

class SetRecurringParams(BaseModel):
    task_id: int
    frequency: str # e.g., "daily", "weekly", "monthly"
    ends_on: Optional[str] = None # YYYY-MM-DD

def validate_set_recurring_params(params: SetRecurringParams) -> dict:
    # Placeholder validation - replace with actual validation logic from .claude/skills
    is_valid = True
    errors = []
    if params.task_id is None:
        is_valid = False
        errors.append({"field": "task_id", "message": "Task ID cannot be empty"})
    if not params.frequency:
        is_valid = False
        errors.append({"field": "frequency", "message": "Frequency cannot be empty"})
    return {"is_valid": is_valid, "errors": errors}


async def set_recurring_tool(user_id: int, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    MCP tool for setting a task as recurring with a specified frequency.

    Args:
        user_id: The ID of the user making the request
        params: Parameters for setting the task as recurring
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
        # Check if task_id and frequency are provided
        if "task_id" not in params or not params["task_id"]:
            return {
                "success": False,
                "error": "validation_error",
                "message": "task_id is required for setting a task as recurring",
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }

        if "frequency" not in params or not params["frequency"]:
            return {
                "success": False,
                "error": "validation_error",
                "message": "frequency is required for setting a task as recurring",
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }

        # Create SetRecurringParams object for validation
        validation_params = SetRecurringParams(**{
            k: v for k, v in params.items()
            if k in ["task_id", "frequency", "ends_on"]
        })

        validation_result = validate_set_recurring_params(validation_params)

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
        skill_name="set_recurring",
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
            context_manager.set_last_task_action(session_id, "set_recurring", task_id)

    return result