"""
Integration module for the MCP (Model Context Protocol) server.

This module provides integration between MCP tools and existing todo skills.
"""
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import logging
import asyncio

# Import real skill implementations
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


class TodoSkillAdapter:
    """
    Adapter class to connect MCP tools with existing todo skills.
    """

    def __init__(self):
        """
        Initialize the adapter with references to todo skills.
        """
        self.skill_functions = {
            "add_task": add_task_skill,
            "view_tasks": view_tasks_skill,
            "update_task": update_task_skill,
            "delete_task": delete_task_skill,
            "mark_complete": mark_complete_skill,
            "search_filter_tasks": search_filter_tasks_skill,
            "set_recurring": set_recurring_skill,
            "get_task_context": get_task_context_skill
        }

    async def execute_add_task(
        self,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute the add_task skill through the adapter.

        Args:
            user_id: The ID of the user
            params: Parameters for the task to add
            session_id: The session ID

        Returns:
            Dict[str, Any]: Result of the operation
        """
        try:
            # Map MCP parameters to skill parameters
            title = params.get("title", "")
            description = params.get("description")
            priority = params.get("priority", "medium")
            due_date = params.get("due_date")
            tags = params.get("tags", [])

            # Call the skill function directly
            result = await add_task_skill(
                user_id=user_id,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                tags=tags
            )

            return result

        except Exception as e:
            logger.error(f"Error executing add_task skill: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to add task",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def execute_view_tasks(
        self,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute the view_tasks skill through the adapter.

        Args:
            user_id: The ID of the user
            params: Parameters for filtering tasks
            session_id: The session ID

        Returns:
            Dict[str, Any]: Result of the operation
        """
        try:
            # Map MCP parameters to skill parameters
            status = params.get("status")
            priority = params.get("priority")
            limit = params.get("limit")
            offset = params.get("offset")
            sort_by = params.get("sort_by", "created_at")
            sort_order = params.get("sort_order", "desc")

            # Call the skill function directly
            result = await view_tasks_skill(
                user_id=user_id,
                status=status,
                priority=priority,
                limit=limit,
                offset=offset,
                sort_by=sort_by,
                sort_order=sort_order
            )

            return result

        except Exception as e:
            logger.error(f"Error executing view_tasks skill: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to view tasks",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def execute_update_task(
        self,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute the update_task skill through the adapter.

        Args:
            user_id: The ID of the user
            params: Parameters for updating the task
            session_id: The session ID

        Returns:
            Dict[str, Any]: Result of the operation
        """
        try:
            # Map MCP parameters to skill parameters
            task_id = params.get("task_id")
            if not task_id:
                return {
                    "success": False,
                    "error": "task_id is required",
                    "message": "Task ID is required to update a task",
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Extract other update parameters
            title = params.get("title")
            description = params.get("description")
            priority = params.get("priority")
            due_date = params.get("due_date")
            completed = params.get("completed")

            # Call the skill function directly
            result = await update_task_skill(
                user_id=user_id,
                task_id=task_id,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                completed=completed
            )

            return result

        except Exception as e:
            logger.error(f"Error executing update_task skill: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update task",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def execute_delete_task(
        self,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute the delete_task skill through the adapter.

        Args:
            user_id: The ID of the user
            params: Parameters for deleting the task
            session_id: The session ID

        Returns:
            Dict[str, Any]: Result of the operation
        """
        try:
            # Map MCP parameters to skill parameters
            task_id = params.get("task_id")
            if not task_id:
                return {
                    "success": False,
                    "error": "task_id is required",
                    "message": "Task ID is required to delete a task",
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Call the skill function directly
            result = await delete_task_skill(
                user_id=user_id,
                task_id=task_id
            )

            return result

        except Exception as e:
            logger.error(f"Error executing delete_task skill: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to delete task",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def execute_mark_complete(
        self,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute the mark_complete skill through the adapter.

        Args:
            user_id: The ID of the user
            params: Parameters for marking the task complete
            session_id: The session ID

        Returns:
            Dict[str, Any]: Result of the operation
        """
        try:
            # Map MCP parameters to skill parameters
            task_id = params.get("task_id")
            completed = params.get("completed", True)

            if not task_id:
                return {
                    "success": False,
                    "error": "task_id is required",
                    "message": "Task ID is required to mark a task complete",
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Call the skill function directly
            result = await mark_complete_skill(
                user_id=user_id,
                task_id=task_id,
                completed=completed
            )

            return result

        except Exception as e:
            logger.error(f"Error executing mark_complete skill: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to mark task complete",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def execute_search_filter_tasks(
        self,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute the search_filter_tasks skill through the adapter.

        Args:
            user_id: The ID of the user
            params: Parameters for searching and filtering tasks
            session_id: The session ID

        Returns:
            Dict[str, Any]: Result of the operation
        """
        try:
            # Map MCP parameters to skill parameters
            query = params.get("query")
            status = params.get("status")
            priority = params.get("priority")
            tags = params.get("tags")
            limit = params.get("limit")
            offset = params.get("offset")
            sort_by = params.get("sort_by", "created_at")
            sort_order = params.get("sort_order", "desc")

            # Call the skill function directly
            result = await search_filter_tasks_skill(
                user_id=user_id,
                query=query,
                status=status,
                priority=priority,
                tags=tags,
                limit=limit,
                offset=offset,
                sort_by=sort_by,
                sort_order=sort_order
            )

            return result

        except Exception as e:
            logger.error(f"Error executing search_filter_tasks skill: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to search/filter tasks",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def execute_set_recurring(
        self,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute the set_recurring skill through the adapter.

        Args:
            user_id: The ID of the user
            params: Parameters for setting recurring tasks
            session_id: The session ID

        Returns:
            Dict[str, Any]: Result of the operation
        """
        try:
            # Map MCP parameters to skill parameters
            task_id = params.get("task_id")
            frequency = params.get("frequency", "daily")
            ends_on = params.get("ends_on")

            if not task_id:
                return {
                    "success": False,
                    "error": "task_id is required",
                    "message": "Task ID is required to set a task as recurring",
                    "timestamp": datetime.utcnow().isoformat()
                }

            # Call the skill function directly
            result = await set_recurring_skill(
                user_id=user_id,
                task_id=task_id,
                frequency=frequency,
                ends_on=ends_on
            )

            return result

        except Exception as e:
            logger.error(f"Error executing set_recurring skill: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to set recurring task",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def execute_get_task_context(
        self,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute the get_task_context skill through the adapter.

        Args:
            user_id: The ID of the user
            params: Parameters for getting task context
            session_id: The session ID

        Returns:
            Dict[str, Any]: Result of the operation
        """
        try:
            # Map MCP parameters to skill parameters
            task_ids = params.get("task_ids")
            recent_count = params.get("recent_count", 5)
            include_completed = params.get("include_completed", False)

            # Call the skill function directly
            result = await get_task_context_skill(
                user_id=user_id,
                task_ids=task_ids,
                recent_count=recent_count,
                include_completed=include_completed
            )

            return result

        except Exception as e:
            logger.error(f"Error executing get_task_context skill: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get task context",
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_skill_function(self, skill_name: str) -> Optional[Callable]:
        """
        Get a reference to a skill function by name.

        Args:
            skill_name: The name of the skill

        Returns:
            Optional[Callable]: The skill function or None if not found
        """
        return self.skill_functions.get(skill_name)


class MCPIntegrationManager:
    """
    Manager class for MCP integration with existing systems.
    """

    def __init__(self):
        """
        Initialize the integration manager.
        """
        self.skill_adapter = TodoSkillAdapter()

    async def execute_skill_via_mcp(
        self,
        skill_name: str,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute a skill via MCP integration.

        Args:
            skill_name: The name of the skill to execute
            user_id: The ID of the user
            params: Parameters for the skill
            session_id: The session ID

        Returns:
            Dict[str, Any]: Result of the operation
        """
        # Map skill names to adapter methods
        skill_method_map = {
            "add_task": self.skill_adapter.execute_add_task,
            "view_tasks": self.skill_adapter.execute_view_tasks,
            "update_task": self.skill_adapter.execute_update_task,
            "delete_task": self.skill_adapter.execute_delete_task,
            "mark_complete": self.skill_adapter.execute_mark_complete,
            "search_filter_tasks": self.skill_adapter.execute_search_filter_tasks,
            "set_recurring": self.skill_adapter.execute_set_recurring,
            "get_task_context": self.skill_adapter.execute_get_task_context
        }

        if skill_name not in skill_method_map:
            return {
                "success": False,
                "error": f"Skill '{skill_name}' not supported via MCP",
                "message": f"The skill '{skill_name}' is not available through MCP",
                "timestamp": datetime.utcnow().isoformat()
            }

        # Execute the appropriate method
        method = skill_method_map[skill_name]
        return await method(user_id, params, session_id)

    def is_skill_available_via_mcp(self, skill_name: str) -> bool:
        """
        Check if a skill is available via MCP integration.

        Args:
            skill_name: The name of the skill

        Returns:
            bool: True if the skill is available via MCP, False otherwise
        """
        return skill_name in [
            "add_task",
            "view_tasks",
            "update_task",
            "delete_task",
            "mark_complete",
            "search_filter_tasks",
            "set_recurring",
            "get_task_context"
        ]

    def get_available_mcp_skills(self) -> list:
        """
        Get a list of all skills available via MCP integration.

        Returns:
            list: List of available skill names
        """
        return [
            "add_task",
            "view_tasks",
            "update_task",
            "delete_task",
            "mark_complete",
            "search_filter_tasks",
            "set_recurring",
            "get_task_context"
        ]


class ChatbotOrchestratorMCPAdapter:
    """
    Adapter for integrating MCP with the ChatbotOrchestratorAgent.
    """

    def __init__(self):
        """
        Initialize the orchestrator adapter.
        """
        self.integration_manager = MCPIntegrationManager()

    async def call_mcp_tool(
        self,
        tool_name: str,
        user_id: int,
        params: Dict[str, Any],
        session_id: str = None
    ) -> Dict[str, Any]:
        """
        Call an MCP tool from the orchestrator.

        Args:
            tool_name: The name of the tool to call
            user_id: The ID of the user
            params: Parameters for the tool
            session_id: The session ID (optional, will be generated if not provided)

        Returns:
            Dict[str, Any]: Result of the tool call
        """
        # Generate session ID if not provided
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())

        # Execute the skill via MCP
        result = await self.integration_manager.execute_skill_via_mcp(
            skill_name=tool_name,
            user_id=user_id,
            params=params,
            session_id=session_id
        )

        return result

    async def batch_call_mcp_tools(
        self,
        tool_calls: list,
        user_id: int,
        session_id: str = None
    ) -> list:
        """
        Batch call multiple MCP tools.

        Args:
            tool_calls: List of tool calls, each with name and params
            user_id: The ID of the user
            session_id: The session ID (optional)

        Returns:
            list: List of results from each tool call
        """
        results = []

        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            params = tool_call.get("params", {})

            result = await self.call_mcp_tool(
                tool_name=tool_name,
                user_id=user_id,
                params=params,
                session_id=session_id
            )

            results.append(result)

        return results


# Global integration manager instance
integration_manager = MCPIntegrationManager()
orchestrator_adapter = ChatbotOrchestratorMCPAdapter()


def get_integration_manager() -> MCPIntegrationManager:
    """
    Get the global integration manager instance.

    Returns:
        MCPIntegrationManager: The integration manager instance
    """
    return integration_manager


def get_orchestrator_adapter() -> ChatbotOrchestratorMCPAdapter:
    """
    Get the global orchestrator adapter instance.

    Returns:
        ChatbotOrchestratorMCPAdapter: The orchestrator adapter instance
    """
    return orchestrator_adapter