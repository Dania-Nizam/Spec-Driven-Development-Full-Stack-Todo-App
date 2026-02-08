"""Skill to retrieve recent task context for follow-up conversations."""

import json
import os
from typing import Dict, Any
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
BETTER_AUTH_TOKEN = os.getenv("BETTER_AUTH_TOKEN")
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")


def get_task_context_skill(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieves recent task context for follow-up conversations.

    Args:
        params: Dictionary containing user ID and retrieval criteria
                - user_id (str, required): The ID of the user whose task context to retrieve
                - limit (int, optional): Maximum number of recent tasks to return (default: 5)
                - include_completed (bool, optional): Whether to include completed tasks (default: false)

    Returns:
        Dict with success status, message, and context array
    """
    try:
        user_id = params.get('user_id')

        if not user_id:
            return {"success": False, "message": "user_id is required"}

        # Get parameters with defaults
        limit = params.get('limit', 5)
        include_completed = params.get('include_completed', False)

        # Make API call to get recent tasks for context
        headers = {
            "Authorization": f"Bearer {BETTER_AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        # Build URL with query parameters
        url = f"{BACKEND_BASE_URL}/api/{user_id}/tasks"

        # Add filters for recent activity
        query_params = f"?sort_by=created_at&order=desc&limit={limit}"

        if not include_completed:
            query_params += "&status=pending,in_progress"

        url += query_params

        response = httpx.get(url, headers=headers)

        if response.status_code == 200:
            tasks = response.json()
            return {
                "success": True,
                "message": f"Retrieved {len(tasks)} recent tasks for context",
                "context": tasks
            }
        else:
            return {
                "success": False,
                "message": f"Failed to retrieve task context: {response.text}",
                "context": []
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving task context: {str(e)}",
            "context": []
        }


# Register the function with OpenAI
def get_openai_tool_definition():
    """Returns the OpenAI tool definition for this skill."""
    return {
        "type": "function",
        "function": {
            "name": "get_task_context_skill",
            "description": "Retrieves recent task context for follow-up conversations",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user whose task context to retrieve"
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 20,
                        "default": 5,
                        "description": "Maximum number of recent tasks to return (default: 5)"
                    },
                    "include_completed": {
                        "type": "boolean",
                        "default": False,
                        "description": "Whether to include completed tasks (default: false)"
                    }
                },
                "required": ["user_id"]
            }
        }
    }