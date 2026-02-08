"""
Simplified MCP SDK Adapter for in-process tool calling.
Provides MCP-style tool interface without requiring stdio server.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Import skill implementations
from .skills_impl import (
    add_task_skill,
    view_tasks_skill,
    update_task_skill,
    delete_task_skill,
    mark_complete_skill,
    search_filter_tasks_skill,
    set_recurring_skill,
    get_task_context_skill
)

logger = logging.getLogger(__name__)


class SimplifiedMCPAdapter:
    """
    Simplified MCP adapter that provides tool calling without full MCP SDK.
    Works in-process for FastAPI integration.
    """

    def __init__(self):
        """Initialize the simplified MCP adapter."""
        self.tools = {
            "add_task": add_task_skill,
            "view_tasks": view_tasks_skill,
            "update_task": update_task_skill,
            "delete_task": delete_task_skill,
            "mark_complete": mark_complete_skill,
            "search_filter_tasks": search_filter_tasks_skill,
            "set_recurring": set_recurring_skill,
            "get_task_context": get_task_context_skill
        }
        logger.info("SimplifiedMCPAdapter initialized with 8 tools")

    async def call_mcp_tool(
        self,
        tool_name: str,
        user_id: int,
        params: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call an MCP tool through the adapter.

        Args:
            tool_name: Name of the tool to call
            user_id: Authenticated user ID
            params: Parameters for the tool (without user_id)
            session_id: Optional session ID for context

        Returns:
            Dict with success status and result/error
        """
        try:
            # Get the tool function
            tool_func = self.tools.get(tool_name)
            if not tool_func:
                return {
                    "success": False,
                    "error": f"Tool '{tool_name}' not found",
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Call the tool with user_id and params
            result = await tool_func(user_id=user_id, **params)

            return result

        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to execute {tool_name}",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def list_available_tools(self) -> list:
        """
        Get list of all available tools.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())


# Global adapter instance
_mcp_adapter = SimplifiedMCPAdapter()


def get_mcp_sdk_adapter() -> SimplifiedMCPAdapter:
    """
    Get the global MCP SDK adapter instance.

    Returns:
        SimplifiedMCPAdapter instance
    """
    return _mcp_adapter
