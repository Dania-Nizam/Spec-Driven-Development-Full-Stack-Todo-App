"""
OpenAI Agents SDK Integration for Todo Chatbot
Uses OpenAI Agents SDK (not just API) to create an intelligent agent that uses MCP tools.
"""
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from openai import AsyncOpenAI
from openai.types.beta import Assistant
from openai.types.beta.threads import Run, Message

logger = logging.getLogger(__name__)


class OpenAIAgentOrchestrator:
    """
    OpenAI Agents SDK orchestrator that uses MCP tools for todo operations.
    Implements proper agent orchestration with tool calling capabilities.
    """

    def __init__(self, api_key: str, mcp_adapter):
        """
        Initialize the OpenAI Agent orchestrator.

        Args:
            api_key: OpenAI API key
            mcp_adapter: MCP SDK adapter for tool execution
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.mcp_adapter = mcp_adapter
        self.assistant: Optional[Assistant] = None
        self.assistant_id: Optional[str] = None

        # Define MCP tools in OpenAI function calling format
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
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
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "view_tasks",
                    "description": "View all tasks for the authenticated user",
                    "parameters": {
                        "type": "object",
                        "properties": {
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
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
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
                            "completed": {
                                "type": "boolean",
                                "description": "Mark task as completed or not"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task from the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "mark_complete",
                    "description": "Mark a task as complete or incomplete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to mark"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "True to mark complete, False to mark incomplete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_filter_tasks",
                    "description": "Search and filter tasks with advanced criteria",
                    "parameters": {
                        "type": "object",
                        "properties": {
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
                            }
                        },
                        "required": []
                    }
                }
            }
        ]

    async def initialize_assistant(self) -> Assistant:
        """
        Initialize or retrieve the OpenAI Assistant.

        Returns:
            Assistant object
        """
        if self.assistant:
            return self.assistant

        try:
            # Create a new assistant with MCP tools
            self.assistant = await self.client.beta.assistants.create(
                name="Todo Chatbot Assistant",
                instructions="""You are a helpful todo list assistant. You help users manage their tasks efficiently.

You can:
- Add new tasks with titles, descriptions, priorities, and due dates
- View all tasks or filter by status/priority
- Update existing tasks
- Delete tasks
- Mark tasks as complete or incomplete
- Search and filter tasks

Always be friendly and helpful. When users ask about their tasks, use the appropriate tools to fetch and display the information. Respond in a natural, conversational way.

If a user mentions a task by number (like "task 1" or "#2"), extract that number as the task_id for operations.

For Urdu-speaking users, you can respond in Urdu if they prefer.""",
                model="gpt-4-turbo-preview",
                tools=self.tools
            )

            self.assistant_id = self.assistant.id
            logger.info(f"Created OpenAI Assistant: {self.assistant_id}")

            return self.assistant

        except Exception as e:
            logger.error(f"Error creating assistant: {str(e)}")
            raise

    async def process_message(
        self,
        user_id: int,
        message: str,
        thread_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user message using OpenAI Agents SDK.

        Args:
            user_id: The authenticated user ID
            message: The user's message
            thread_id: Optional thread ID for conversation continuity

        Returns:
            Dict with response, thread_id, and success status
        """
        try:
            # Initialize assistant if needed
            await self.initialize_assistant()

            # Create or use existing thread
            if thread_id:
                thread = await self.client.beta.threads.retrieve(thread_id)
            else:
                thread = await self.client.beta.threads.create()
                thread_id = thread.id

            # Add user message to thread
            await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )

            # Run the assistant
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id
            )

            # Wait for completion and handle tool calls
            response_text = await self._handle_run(run, thread_id, user_id)

            return {
                "message": response_text,
                "thread_id": thread_id,
                "success": True,
                "conversation_context": {
                    "thread_id": thread_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "message": f"معذرت، ایک خرابی ہوئی: {str(e)}",
                "success": False,
                "error": str(e)
            }

    async def _handle_run(
        self,
        run: Run,
        thread_id: str,
        user_id: int
    ) -> str:
        """
        Handle the assistant run, including tool calls.

        Args:
            run: The Run object
            thread_id: Thread ID
            user_id: User ID for tool execution

        Returns:
            Final response text
        """
        max_iterations = 10
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Poll for run status
            run = await self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

            if run.status == "completed":
                # Get the assistant's response
                messages = await self.client.beta.threads.messages.list(
                    thread_id=thread_id,
                    order="desc",
                    limit=1
                )

                if messages.data:
                    message = messages.data[0]
                    if message.content:
                        return message.content[0].text.value

                return "Task completed successfully."

            elif run.status == "requires_action":
                # Handle tool calls
                tool_outputs = []

                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    logger.info(f"Calling MCP tool: {function_name} with args: {function_args}")

                    # Execute the MCP tool
                    result = await self.mcp_adapter.call_mcp_tool(
                        tool_name=function_name,
                        user_id=user_id,
                        params=function_args
                    )

                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(result)
                    })

                # Submit tool outputs
                run = await self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

            elif run.status in ["failed", "cancelled", "expired"]:
                logger.error(f"Run failed with status: {run.status}")
                return f"معذرت، کام مکمل نہیں ہو سکا۔ Status: {run.status}"

            # Wait a bit before polling again
            await asyncio.sleep(0.5)

        return "معذرت، جواب دینے میں بہت وقت لگ گیا۔"
