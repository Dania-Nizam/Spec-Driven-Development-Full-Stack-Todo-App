"""Skill to update an existing todo task."""

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


def update_task_skill(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates an existing todo task via the backend API with JWT authentication.

    Args:
        params: Dictionary containing update criteria and new values
                - task_id (str, required): The ID of the task to update
                - title (str, optional): New title of the task
                - description (str, optional): New detailed description
                - priority (str, optional): New priority level
                - tags (list, optional): New array of tags
                - due_date (str, optional): New due date
                - recurrence (str, optional): New recurrence pattern
                - status (str, optional): New status

    Returns:
        Dict with success status and message
    """
    try:
        task_id = params.get('task_id')

        if not task_id:
            return {"success": False, "message": "task_id is required"}

        # Get user_id from JWT token context (simplified for this example)
        user_id = "1"  # This should come from decoded JWT

        # Prepare update payload (only include provided fields)
        update_data = {}
        if 'title' in params:
            update_data['title'] = params['title']
        if 'description' in params:
            update_data['description'] = params['description']
        if 'priority' in params:
            update_data['priority'] = params['priority']
        if 'tags' in params:
            update_data['tags'] = params['tags']
        if 'due_date' in params:
            update_data['due_date'] = params['due_date']
        if 'recurrence' in params:
            update_data['recurrence'] = params['recurrence']
        if 'status' in params:
            update_data['status'] = params['status']

        if not update_data:
            return {"success": False, "message": "No fields to update provided"}

        # Make API call to update the task
        headers = {
            "Authorization": f"Bearer {BETTER_AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"{BACKEND_BASE_URL}/api/{user_id}/tasks/{task_id}"

        response = httpx.patch(url, json=update_data, headers=headers)

        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Task with ID '{task_id}' updated successfully"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "message": f"Task with ID '{task_id}' not found"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to update task: {response.text}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating task: {str(e)}"
        }


# Register the function with OpenAI
def get_openai_tool_definition():
    """Returns the OpenAI tool definition for this skill."""
    return {
        "type": "function",
        "function": {
            "name": "update_task_skill",
            "description": "Updates an existing todo task in the user's task list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "New detailed description of the task"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "New priority level of the task"
                    },
                    "tags": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "New array of tag strings"
                    },
                    "due_date": {
                        "type": "string",
                        "format": "date",
                        "description": "New due date in YYYY-MM-DD format"
                    },
                    "recurrence": {
                        "type": "string",
                        "enum": ["daily", "weekly", "monthly", "yearly"],
                        "description": "New recurrence pattern"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed"],
                        "description": "New status of the task"
                    }
                },
                "required": ["task_id"]
            }
        }
    }