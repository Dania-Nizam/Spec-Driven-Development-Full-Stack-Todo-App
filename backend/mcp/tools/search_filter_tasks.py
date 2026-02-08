"""
MCP Tool: Search and Filter Tasks

This module implements the search_filter_tasks MCP tool that integrates with the
existing search_filter_tasks_skill to search and filter tasks.
"""
from typing import Dict, Any
from pydantic import BaseModel
from typing import Optional, List
from backend.mcp.models import MCPTaskStatus, MCPTaskPriority

class SearchFilterTasksParams(BaseModel):
    query: Optional[str] = None
    status: Optional[MCPTaskStatus] = MCPTaskStatus.ALL
    priority: Optional[MCPTaskPriority] = None
    tags: Optional[List[str]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"

def validate_search_filter_tasks_params(params: SearchFilterTasksParams) -> dict:
    # Placeholder validation - replace with actual validation logic from .claude/skills
    is_valid = True
    errors = []
    return {"is_valid": is_valid, "errors": errors}


async def search_filter_tasks_tool(user_id: int, params: Dict[str, Any], session_id: str) -> Dict[str, Any]:
    """
    MCP tool for searching and filtering the user's tasks based on various criteria.

    Args:
        user_id: The ID of the user making the request
        params: Parameters for searching and filtering tasks
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
        # Create SearchFilterTasksParams object for validation
        validation_params = SearchFilterTasksParams(**{
            k: v for k, v in params.items()
            if k in ["query", "status", "priority", "tags", "limit", "offset", "sort_by", "sort_order"]
        })

        validation_result = validate_search_filter_tasks_params(validation_params)

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
        skill_name="search_filter_tasks",
        user_id=user_id,
        params=params,
        session_id=session_id
    )

    # Update context if successful
    if result.get("success"):
        task_ids = [task.get("id") for task in result.get("result", {}).get("tasks", [])]
        if task_ids:
            context_manager = get_context_manager()
            for task_id in task_ids:
                context_manager.reference_task(session_id, task_id)

            context_manager.set_last_task_action(session_id, "search")
            context_manager.set_current_topic(session_id, "task searching")

    return result