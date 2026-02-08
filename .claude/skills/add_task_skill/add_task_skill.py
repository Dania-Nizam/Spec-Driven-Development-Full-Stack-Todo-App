"""Skill to add a new todo task."""

import json
import os
from typing import Dict, Any, Optional
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BETTER_AUTH_TOKEN = os.getenv("BETTER_AUTH_TOKEN")
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")


def add_task_skill(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adds a new todo task via the backend API with JWT authentication.

    Args:
        params: Dictionary containing task details
                - title (str, required): The title of the task
                - description (str, optional): Detailed description of the task
                - priority (str, optional): Priority level (low, medium, high)
                - tags (list, optional): Array of tag strings
                - due_date (str, optional): Due date in YYYY-MM-DD format
                - recurrence (str, optional): Recurrence pattern

    Returns:
        Dict with success status, message, and optional task_id
    """
    try:
        # Validate required parameters
        if not params.get('title'):
            return {"success": False, "message": "Title is required"}

        title = params['title']
        description = params.get('description', '')
        priority = params.get('priority', 'medium')
        tags = params.get('tags', [])
        due_date = params.get('due_date')
        recurrence = params.get('recurrence')

        # Get user_id from JWT token context (simplified for this example)
        # In a real implementation, you'd decode the JWT to get the user_id
        # For now, assuming the token contains user information
        user_id = "1"  # This should come from decoded JWT

        # Prepare request payload
        payload = {
            "title": title,
            "description": description,
            "priority": priority,
            "tags": tags,
            "due_date": due_date,
            "recurrence": recurrence
        }

        # Make API call to backend
        headers = {
            "Authorization": f"Bearer {BETTER_AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"{BACKEND_BASE_URL}/api/{user_id}/tasks"

        response = httpx.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            task_data = response.json()
            return {
                "success": True,
                "message": f"Task '{title}' added successfully",
                "task_id": task_data.get("id")
            }
        else:
            return {
                "success": False,
                "message": f"Failed to add task: {response.text}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error adding task: {str(e)}"
        }


# Register the function with OpenAI
def get_openai_tool_definition():
    """Returns the OpenAI tool definition for this skill."""
    return {
        "type": "function",
        "function": {
            "name": "add_task_skill",
            "description": "Adds a new todo task to the user's task list",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the task"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority level of the task"
                    },
                    "tags": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Array of tag strings"
                    },
                    "due_date": {
                        "type": "string",
                        "format": "date",
                        "description": "Due date in YYYY-MM-DD format"
                    },
                    "recurrence": {
                        "type": "string",
                        "enum": ["daily", "weekly", "monthly", "yearly"],
                        "description": "Recurrence pattern"
                    }
                },
                "required": ["title"]
            }
        }
    }