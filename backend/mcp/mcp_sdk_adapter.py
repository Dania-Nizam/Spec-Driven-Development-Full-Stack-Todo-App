"""
Adapter to integrate Official MCP SDK Server with FastAPI Chat Endpoint.
Provides a bridge between the stateless chat API and the MCP SDK server.
"""
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .mcp_sdk_server import server as mcp_server

logger = logging.getLogger(__name__)


class MCPSDKAdapter:
    """
    Adapter class that bridges FastAPI chat endpoint with Official MCP SDK server.
    Allows calling MCP tools without stdio transport for in-process communication.
    """

    def __init__(self):
        """Initialize the MCP SDK adapter."""
        self.mcp_server = mcp_server
        logger.info("MCPSDKAdapter initialized with Official MCP SDK server")

    async def list_available_tools(self) -> list:
        """
        Get list of all available MCP tools.

        Returns:
            List of tool definitions from the MCP server
        """
        try:
            tools = await self.mcp_server._list_tools_handler()
            return [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                for tool in tools
            ]
        except Exception as e:
            logger.error(f"Error listing MCP tools: {str(e)}")
            return []

    async def call_mcp_tool(
        self,
        tool_name: str,
        user_id: int,
        params: Dict[str, Any],
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call an MCP tool through the Official SDK server.

        Args:
            tool_name: Name of the tool to call
            user_id: Authenticated user ID
            params: Parameters for the tool (without user_id)
            session_id: Optional session ID for context

        Returns:
            Dict with success status and result/error
        """
        try:
            # Add user_id to params
            arguments = {**params, "user_id": user_id}

            # Call the MCP server's tool handler
            result_contents = await self.mcp_server._call_tool_handler(
                name=tool_name,
                arguments=arguments
            )

            # Extract text content from MCP response
            if result_contents and len(result_contents) > 0:
                import json
                result_text = result_contents[0].text

                # Try to parse as JSON
                try:
                    result_data = json.loads(result_text)
                    return result_data
                except json.JSONDecodeError:
                    # If not JSON, return as plain text
                    return {
                        "success": True,
                        "message": result_text,
                        "timestamp": datetime.utcnow().isoformat()
                    }
            else:
                return {
                    "success": False,
                    "error": "No response from MCP tool",
                    "timestamp": datetime.utcnow().isoformat()
                }

        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to execute {tool_name}",
                "timestamp": datetime.utcnow().isoformat()
            }

    async def execute_tool_with_context(
        self,
        tool_name: str,
        user_id: int,
        params: Dict[str, Any],
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool with conversation context support.

        Args:
            tool_name: Name of the tool to call
            user_id: Authenticated user ID
            params: Parameters for the tool
            conversation_id: Optional conversation ID for persistence

        Returns:
            Dict with success status and result
        """
        # For now, just call the tool directly
        # In Step 4, we'll add conversation persistence here
        result = await self.call_mcp_tool(
            tool_name=tool_name,
            user_id=user_id,
            params=params,
            session_id=str(conversation_id) if conversation_id else None
        )

        return result

    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the input schema for a specific tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool schema or None if not found
        """
        # This would need to be implemented by caching the tools list
        # For now, return None
        return None


# Global adapter instance
mcp_sdk_adapter = MCPSDKAdapter()


def get_mcp_sdk_adapter() -> MCPSDKAdapter:
    """
    Get the global MCP SDK adapter instance.

    Returns:
        MCPSDKAdapter instance
    """
    return mcp_sdk_adapter
