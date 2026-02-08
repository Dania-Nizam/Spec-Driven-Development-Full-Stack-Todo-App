"""
MCP Tool: Get Task Context

This module implements the get_task_context MCP tool that integrates with the
existing get_task_context_skill to retrieve task context.
"""
from typing import Dict, Any
from pydantic import BaseModel
from typing import Optional, List

class GetTaskContextParams(BaseModel):
    task_ids: Optional[List[int]] = None
    recent_count: Optional[int] = 5
    include_completed: Optional[bool] = False

def validate_get_task_context_params(params: GetTaskContextParams) -> dict:
    # Placeholder validation - replace with actual validation logic from .claude/skills
    is_valid = True
    errors = []
    # Add validation logic if necessary
    return {"is_valid": is_valid, "errors": errors}


async def get_task_context_tool(user_id: int, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    MCP tool for getting contextual information about tasks to enhance responses.

    Args:
        user_id: The ID of the user making the request
        params: Parameters for getting task context
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
        # Create GetTaskContextParams object for validation
        validation_params = GetTaskContextParams(**{
            k: v for k, v in params.items()
            if k in ["task_ids", "recent_count", "include_completed"]
        })

        validation_result = validate_get_task_context_params(validation_params)

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
        skill_name="get_task_context",
        user_id=user_id,
        params=params,
        session_id=session_id
    )

    # Update context if successful
    if result.get("success"):
        task_ids = params.get("task_ids", [])
        if task_ids:
            context_manager = get_context_manager()
            for task_id in task_ids:
                context_manager.reference_task(session_id, task_id)

        context_manager.set_last_task_action(session_id, "get_context")

    return result