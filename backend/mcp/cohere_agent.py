"""
Cohere API Integration for Todo Chatbot
Uses Cohere's chat API with tool calling for natural language understanding.
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

import cohere
from cohere.types import Tool, ToolParameterDefinitionsValue

logger = logging.getLogger(__name__)


class CohereAgentOrchestrator:
    """
    Cohere API orchestrator that uses tool calling for todo operations.
    Implements intelligent conversation with natural language understanding.
    """

    def __init__(self, api_key: str, mcp_adapter):
        """
        Initialize the Cohere Agent orchestrator.

        Args:
            api_key: Cohere API key
            mcp_adapter: MCP SDK adapter for tool execution
        """
        self.client = cohere.Client(api_key=api_key)
        self.mcp_adapter = mcp_adapter

        # Define tools in Cohere format
        self.tools = [
            Tool(
                name="add_task",
                description="Add a new task to the user's todo list",
                parameter_definitions={
                    "title": ToolParameterDefinitionsValue(
                        description="The title of the task",
                        type="string",
                        required=True
                    ),
                    "description": ToolParameterDefinitionsValue(
                        description="Optional description of the task",
                        type="string",
                        required=False
                    ),
                    "priority": ToolParameterDefinitionsValue(
                        description="Priority level of the task",
                        type="string",
                        required=False
                    ),
                    "due_date": ToolParameterDefinitionsValue(
                        description="Optional due date in ISO format",
                        type="string",
                        required=False
                    )
                }
            ),
            Tool(
                name="view_tasks",
                description="View all tasks for the authenticated user",
                parameter_definitions={
                    "status": ToolParameterDefinitionsValue(
                        description="Filter by task status (completed, pending, all)",
                        type="string",
                        required=False
                    ),
                    "priority": ToolParameterDefinitionsValue(
                        description="Filter by priority (low, medium, high)",
                        type="string",
                        required=False
                    ),
                    "limit": ToolParameterDefinitionsValue(
                        description="Maximum number of tasks to return",
                        type="number",
                        required=False
                    )
                }
            ),
            Tool(
                name="update_task",
                description="Update an existing task",
                parameter_definitions={
                    "task_id": ToolParameterDefinitionsValue(
                        description="The ID of the task to update",
                        type="number",
                        required=True
                    ),
                    "title": ToolParameterDefinitionsValue(
                        description="New title for the task",
                        type="string",
                        required=False
                    ),
                    "description": ToolParameterDefinitionsValue(
                        description="New description for the task",
                        type="string",
                        required=False
                    ),
                    "priority": ToolParameterDefinitionsValue(
                        description="New priority level",
                        type="string",
                        required=False
                    ),
                    "completed": ToolParameterDefinitionsValue(
                        description="Mark task as completed or not",
                        type="boolean",
                        required=False
                    )
                }
            ),
            Tool(
                name="delete_task",
                description="Delete a task from the user's todo list",
                parameter_definitions={
                    "task_id": ToolParameterDefinitionsValue(
                        description="The ID of the task to delete",
                        type="number",
                        required=True
                    )
                }
            ),
            Tool(
                name="mark_complete",
                description="Mark a task as complete or incomplete",
                parameter_definitions={
                    "task_id": ToolParameterDefinitionsValue(
                        description="The ID of the task to mark",
                        type="number",
                        required=True
                    ),
                    "completed": ToolParameterDefinitionsValue(
                        description="True to mark complete, False to mark incomplete",
                        type="boolean",
                        required=False
                    )
                }
            ),
            Tool(
                name="search_filter_tasks",
                description="Search and filter tasks with advanced criteria",
                parameter_definitions={
                    "query": ToolParameterDefinitionsValue(
                        description="Search query for task title/description",
                        type="string",
                        required=False
                    ),
                    "status": ToolParameterDefinitionsValue(
                        description="Filter by status",
                        type="string",
                        required=False
                    ),
                    "priority": ToolParameterDefinitionsValue(
                        description="Filter by priority",
                        type="string",
                        required=False
                    )
                }
            )
        ]

        # System message for Cohere
        self.preamble = """You are a helpful todo list assistant. You help users manage their tasks efficiently.

You can:
- Add new tasks with titles, descriptions, priorities, and due dates
- View all tasks or filter by status/priority
- Update existing tasks
- Delete tasks
- Mark tasks as complete or incomplete
- Search and filter tasks

Always be friendly and helpful. When users ask about their tasks, use the appropriate tools to fetch and display the information. Respond in a natural, conversational way.

If a user mentions a task by number (like "task 1" or "#2"), extract that number as the task_id for operations.

IMPORTANT: Always respond in English only. Do not use Urdu or any other language."""

    async def process_message(
        self,
        user_id: int,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message using Cohere's chat API.

        Args:
            user_id: The authenticated user ID
            message: The user's message
            conversation_history: Optional conversation history

        Returns:
            Dict with response and success status
        """
        try:
            # Prepare chat history
            chat_history = conversation_history or []

            # Call Cohere chat with tools
            response = self.client.chat(
                message=message,
                chat_history=chat_history,
                tools=self.tools,
                preamble=self.preamble,
                model="command-r-08-2024"  # Current Cohere model with tool support
            )

            logger.info(f"Cohere response received. Has tool calls: {bool(response.tool_calls)}")
            if response.tool_calls:
                logger.info(f"Number of tool calls: {len(response.tool_calls)}")

            # Handle tool calls if any
            if response.tool_calls:
                tool_results = []

                for tool_call in response.tool_calls:
                    tool_name = tool_call.name
                    tool_params = tool_call.parameters

                    logger.info(f"Calling tool: {tool_name} with params: {tool_params}")

                    # Execute the MCP tool
                    result = await self.mcp_adapter.call_mcp_tool(
                        tool_name=tool_name,
                        user_id=user_id,
                        params=tool_params
                    )

                    tool_results.append({
                        "call": tool_call,
                        "outputs": [{"result": json.dumps(result)}]
                    })

                # Get final response with tool results
                # Pass empty message when submitting tool_results
                final_response = self.client.chat(
                    message="",  # Empty message when submitting tool results
                    chat_history=chat_history,
                    tools=self.tools,
                    tool_results=tool_results,
                    preamble=self.preamble,
                    model="command-r-08-2024"
                )

                response_text = final_response.text
            else:
                response_text = response.text

            # Update chat history
            updated_history = chat_history + [
                {"role": "USER", "message": message},
                {"role": "CHATBOT", "message": response_text}
            ]

            return {
                "message": response_text,
                "success": True,
                "conversation_history": updated_history,
                "conversation_context": {
                    "timestamp": datetime.utcnow().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"Error processing message with Cohere: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {repr(e)}")
            return {
                "message": f"معذرت، ایک خرابی ہوئی: {str(e)}",
                "success": False,
                "error": str(e)
            }
