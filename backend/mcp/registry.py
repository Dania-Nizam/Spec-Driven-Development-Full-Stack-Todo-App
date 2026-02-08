"""
Tool registry module for the MCP (Model Context Protocol) server.

This module manages the registration and execution of MCP tools.
"""
from typing import Dict, Any, Callable, Optional, Awaitable, List
from functools import wraps
import logging
import asyncio
from datetime import datetime


logger = logging.getLogger(__name__)


class ToolNotFoundError(Exception):
    """Exception raised when a tool is not found in the registry."""
    pass


class ToolRegistrationError(Exception):
    """Exception raised when there's an error registering a tool."""
    pass


class ToolRegistry:
    """
    Registry for managing MCP tools.
    """

    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: Dict[str, Dict[str, Any]] = {}
        self.tool_descriptions: Dict[str, str] = {}
        self.tool_execution_stats: Dict[str, Dict[str, Any]] = {}

    def register_tool(
        self,
        name: str,
        func: Callable,
        description: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a new tool in the registry.

        Args:
            name: The name of the tool
            func: The function to execute when the tool is called
            description: Optional description of the tool
            schema: Optional JSON schema for the tool's parameters
        """
        if not name or not isinstance(name, str):
            raise ToolRegistrationError("Tool name must be a non-empty string")

        if not callable(func):
            raise ToolRegistrationError("Tool function must be callable")

        # Normalize the tool name to lowercase
        normalized_name = name.lower().strip()

        # Check if tool already exists
        if normalized_name in self.tools:
            logger.warning(f"Tool {normalized_name} already exists, overwriting")

        # Register the tool
        self.tools[normalized_name] = func
        self.tool_descriptions[normalized_name] = description or f"Tool: {normalized_name}"

        if schema:
            self.tool_schemas[normalized_name] = schema
        else:
            # Generate basic schema from function signature if not provided
            self.tool_schemas[normalized_name] = self._generate_basic_schema(func)

        # Initialize stats for the tool
        self.tool_execution_stats[normalized_name] = {
            "calls": 0,
            "successes": 0,
            "failures": 0,
            "total_duration": 0.0,
            "avg_duration": 0.0,
            "last_called": None
        }

        logger.info(f"Registered tool: {normalized_name}")

    def _generate_basic_schema(self, func: Callable) -> Dict[str, Any]:
        """
        Generate a basic JSON schema from a function's signature.

        Args:
            func: The function to generate schema for

        Returns:
            Dict[str, Any]: Basic JSON schema
        """
        # This is a simplified implementation
        # In a real scenario, we'd use inspect to get function parameters
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    def is_tool_registered(self, name: str) -> bool:
        """
        Check if a tool is registered.

        Args:
            name: The name of the tool

        Returns:
            bool: True if the tool is registered, False otherwise
        """
        return name.lower().strip() in self.tools

    async def execute_tool(
        self,
        tool_name: str,
        user_id: int,
        params: Dict[str, Any],
        session_id: str
    ) -> Dict[str, Any]:
        """
        Execute a registered tool with the given parameters.

        Args:
            tool_name: The name of the tool to execute
            user_id: The ID of the user executing the tool
            params: Parameters to pass to the tool
            session_id: The session ID for the execution

        Returns:
            Dict[str, Any]: Result of the tool execution
        """
        normalized_name = tool_name.lower().strip()

        # Check if tool exists
        if normalized_name not in self.tools:
            raise ToolNotFoundError(f"Tool '{tool_name}' is not registered")

        # Get the tool function
        tool_func = self.tools[normalized_name]

        # Update stats
        stats = self.tool_execution_stats[normalized_name]
        stats["calls"] += 1
        stats["last_called"] = datetime.utcnow()

        start_time = asyncio.get_event_loop().time()

        try:
            # Execute the tool function
            # The tool function should accept user_id, params, and session_id
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(user_id, params, session_id)
            else:
                # If it's not an async function, run it in a thread pool
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, tool_func, user_id, params, session_id)

            # Update success stats
            stats["successes"] += 1
            duration = asyncio.get_event_loop().time() - start_time
            stats["total_duration"] += duration
            stats["avg_duration"] = stats["total_duration"] / stats["successes"]

            logger.info(f"Successfully executed tool '{normalized_name}' for user {user_id}")

            return {
                "success": True,
                "result": result,
                "tool_name": normalized_name,
                "execution_time": duration
            }

        except Exception as e:
            # Update failure stats
            stats["failures"] += 1
            duration = asyncio.get_event_loop().time() - start_time
            logger.error(f"Failed to execute tool '{normalized_name}' for user {user_id}: {str(e)}")

            return {
                "success": False,
                "error": str(e),
                "tool_name": normalized_name,
                "execution_time": duration
            }

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get a list of all available tools with their descriptions and schemas.

        Returns:
            List[Dict[str, Any]]: List of available tools
        """
        tools_list = []
        for name in self.tools.keys():
            tools_list.append({
                "name": name,
                "description": self.tool_descriptions[name],
                "parameters": self.tool_schemas[name]
            })
        return tools_list

    def get_tool_names(self) -> List[str]:
        """
        Get a list of all registered tool names.

        Returns:
            List[str]: List of tool names
        """
        return list(self.tools.keys())

    def get_tool_stats(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get execution statistics for a specific tool.

        Args:
            tool_name: The name of the tool

        Returns:
            Optional[Dict[str, Any]]: Tool statistics or None if tool doesn't exist
        """
        normalized_name = tool_name.lower().strip()
        if normalized_name in self.tool_execution_stats:
            return self.tool_execution_stats[normalized_name].copy()
        return None

    def get_all_tool_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get execution statistics for all tools.

        Returns:
            Dict[str, Dict[str, Any]]: All tool statistics
        """
        return {name: stats.copy() for name, stats in self.tool_execution_stats.items()}

    def unregister_tool(self, name: str) -> bool:
        """
        Unregister a tool from the registry.

        Args:
            name: The name of the tool to unregister

        Returns:
            bool: True if unregistered successfully, False otherwise
        """
        normalized_name = name.lower().strip()
        if normalized_name in self.tools:
            del self.tools[normalized_name]
            if normalized_name in self.tool_descriptions:
                del self.tool_descriptions[normalized_name]
            if normalized_name in self.tool_schemas:
                del self.tool_schemas[normalized_name]
            if normalized_name in self.tool_execution_stats:
                del self.tool_execution_stats[normalized_name]

            logger.info(f"Unregistered tool: {normalized_name}")
            return True
        return False

    def clear_registry(self) -> None:
        """
        Clear all registered tools from the registry.
        """
        self.tools.clear()
        self.tool_descriptions.clear()
        self.tool_schemas.clear()
        self.tool_execution_stats.clear()
        logger.info("Cleared tool registry")


class ToolDecorator:
    """
    Decorator for registering tools with the registry.
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def register(
        self,
        name: str,
        description: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None
    ):
        """
        Decorator to register a function as an MCP tool.

        Args:
            name: The name of the tool
            description: Optional description of the tool
            schema: Optional JSON schema for the tool's parameters
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            # Register the tool
            self.registry.register_tool(name, wrapper, description, schema)
            return wrapper

        return decorator


# Global tool registry instance
tool_registry = ToolRegistry()
tool_decorator = ToolDecorator(tool_registry)

# Convenience decorators
register_tool = tool_decorator.register


def get_tool_registry() -> ToolRegistry:
    """
    Get the global tool registry instance.

    Returns:
        ToolRegistry: The tool registry instance
    """
    return tool_registry


# Example usage of the decorator (commented out as we'll import tools separately)
'''
@register_tool(
    name="example_tool",
    description="An example tool for demonstration",
    schema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "An example parameter"}
        },
        "required": ["param1"]
    }
)
async def example_tool(user_id: int, params: Dict[str, Any], session_id: str):
    """
    Example tool implementation.
    """
    param1 = params.get("param1", "default_value")
    return {
        "message": f"Example tool executed with param1: {param1}",
        "user_id": user_id,
        "session_id": session_id
    }
'''