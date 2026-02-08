"""
Official MCP SDK Server for Todo Chatbot
Uses the official mcp Python SDK as required by Hackathon II specification.
"""
import asyncio
import logging
from typing import Any, Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("todo-chatbot-mcp-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available MCP tools following the official SDK format.

    Returns:
        List of Tool objects with proper schemas
    """
    return [
        Tool(
            name="add_task",
            description="Add a new task to the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "The title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority level of the task"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Optional due date in ISO format"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional tags for the task"
                    }
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="view_tasks",
            description="View all tasks for the authenticated user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user ID"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["completed", "pending", "all"],
                        "description": "Filter by task status"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Filter by priority"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of tasks to return"
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of tasks to skip"
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["created_at", "updated_at", "priority", "due_date"],
                        "description": "Field to sort by"
                    },
                    "sort_order": {
                        "type": "string",
                        "enum": ["asc", "desc"],
                        "description": "Sort order"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update an existing task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "New priority level"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in ISO format"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "Mark task as completed or not"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task from the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="mark_complete",
            description="Mark a task as complete or incomplete",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to mark"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "True to mark complete, False to mark incomplete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="search_filter_tasks",
            description="Search and filter tasks with advanced criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user ID"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query for task title/description"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["completed", "pending", "all"],
                        "description": "Filter by status"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Filter by priority"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by tags"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results"
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Results to skip"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="set_recurring",
            description="Set a task as recurring with specified frequency",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user ID"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to make recurring"
                    },
                    "frequency": {
                        "type": "string",
                        "enum": ["daily", "weekly", "monthly", "yearly"],
                        "description": "Recurrence frequency"
                    },
                    "ends_on": {
                        "type": "string",
                        "description": "Optional end date in ISO format"
                    }
                },
                "required": ["user_id", "task_id", "frequency"]
            }
        ),
        Tool(
            name="get_task_context",
            description="Get context about previous tasks for context-aware responses",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The authenticated user ID"
                    },
                    "task_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "Specific task IDs to get context for"
                    },
                    "recent_count": {
                        "type": "integer",
                        "description": "Number of recent tasks to include"
                    },
                    "include_completed": {
                        "type": "boolean",
                        "description": "Whether to include completed tasks"
                    }
                },
                "required": ["user_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """
    Handle tool calls using the official MCP SDK format.

    Args:
        name: The name of the tool to call
        arguments: The arguments for the tool

    Returns:
        List of TextContent with the result
    """
    try:
        # Extract user_id from arguments
        user_id = arguments.get("user_id")
        if not user_id:
            return [TextContent(
                type="text",
                text=f"Error: user_id is required for all tool calls"
            )]

        # Route to appropriate skill implementation
        result = None

        if name == "add_task":
            result = await add_task_skill(
                user_id=user_id,
                title=arguments.get("title"),
                description=arguments.get("description"),
                priority=arguments.get("priority", "medium"),
                due_date=arguments.get("due_date"),
                tags=arguments.get("tags", [])
            )

        elif name == "view_tasks":
            result = await view_tasks_skill(
                user_id=user_id,
                status=arguments.get("status"),
                priority=arguments.get("priority"),
                limit=arguments.get("limit"),
                offset=arguments.get("offset"),
                sort_by=arguments.get("sort_by", "created_at"),
                sort_order=arguments.get("sort_order", "desc")
            )

        elif name == "update_task":
            result = await update_task_skill(
                user_id=user_id,
                task_id=arguments.get("task_id"),
                title=arguments.get("title"),
                description=arguments.get("description"),
                priority=arguments.get("priority"),
                due_date=arguments.get("due_date"),
                completed=arguments.get("completed")
            )

        elif name == "delete_task":
            result = await delete_task_skill(
                user_id=user_id,
                task_id=arguments.get("task_id")
            )

        elif name == "mark_complete":
            result = await mark_complete_skill(
                user_id=user_id,
                task_id=arguments.get("task_id"),
                completed=arguments.get("completed", True)
            )

        elif name == "search_filter_tasks":
            result = await search_filter_tasks_skill(
                user_id=user_id,
                query=arguments.get("query"),
                status=arguments.get("status"),
                priority=arguments.get("priority"),
                tags=arguments.get("tags"),
                limit=arguments.get("limit"),
                offset=arguments.get("offset"),
                sort_by=arguments.get("sort_by", "created_at"),
                sort_order=arguments.get("sort_order", "desc")
            )

        elif name == "set_recurring":
            result = await set_recurring_skill(
                user_id=user_id,
                task_id=arguments.get("task_id"),
                frequency=arguments.get("frequency", "daily"),
                ends_on=arguments.get("ends_on")
            )

        elif name == "get_task_context":
            result = await get_task_context_skill(
                user_id=user_id,
                task_ids=arguments.get("task_ids"),
                recent_count=arguments.get("recent_count", 5),
                include_completed=arguments.get("include_completed", False)
            )

        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )]

        # Format result as TextContent
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, default=str)
        )]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return [TextContent(
            type="text",
            text=f"Error executing {name}: {str(e)}"
        )]


async def main():
    """
    Main entry point for the MCP server using stdio transport.
    This follows the official MCP SDK pattern.
    """
    logger.info("Starting Official MCP SDK Server for Todo Chatbot...")

    # Run the server with stdio transport (standard for MCP)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    # Run the server
    asyncio.run(main())
