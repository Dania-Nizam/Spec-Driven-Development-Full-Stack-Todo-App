"""Skill to set or update the recurring pattern of a todo task."""

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


def set_recurring_skill(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sets or updates the recurring pattern of a todo task via the backend API with JWT authentication.

    Args:
        params: Dictionary containing task ID and recurrence details
                - task_id (str, required): The ID of the task to update
                - recurrence_pattern (str, required): The recurrence pattern (daily, weekly, monthly, yearly)
                - recurrence_end_date (str, optional): End date for the recurrence in YYYY-MM-DD format
                - recurrence_interval (int, optional): Interval for the recurrence (e.g., every 2 weeks)

    Returns:
        Dict with success status and message
    """
    try:
        task_id = params.get('task_id')
        recurrence_pattern = params.get('recurrence_pattern')

        if not task_id:
            return {"success": False, "message": "task_id is required"}

        if not recurrence_pattern:
            return {"success": False, "message": "recurrence_pattern is required"}

        # Get user_id from JWT token context (simplified for this example)
        user_id = "1"  # This should come from decoded JWT

        # Prepare update payload
        update_data = {"recurrence": recurrence_pattern}

        if params.get('recurrence_end_date'):
            update_data['recurrence_end_date'] = params['recurrence_end_date']

        if params.get('recurrence_interval') is not None:
            update_data['recurrence_interval'] = params['recurrence_interval']

        # Make API call to update the task recurrence
        headers = {
            "Authorization": f"Bearer {BETTER_AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"{BACKEND_BASE_URL}/api/{user_id}/tasks/{task_id}"

        response = httpx.patch(url, json=update_data, headers=headers)

        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Recurring pattern for task with ID '{task_id}' updated successfully"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "message": f"Task with ID '{task_id}' not found"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to update task recurrence: {response.text}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating task recurrence: {str(e)}"
        }


# Register the function with OpenAI
def get_openai_tool_definition():
    """Returns the OpenAI tool definition for this skill."""
    return {
        "type": "function",
        "function": {
            "name": "set_recurring_skill",
            "description": "Sets or updates the recurring pattern of a todo task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update"
                    },
                    "recurrence_pattern": {
                        "type": "string",
                        "enum": ["daily", "weekly", "monthly", "yearly"],
                        "description": "The recurrence pattern"
                    },
                    "recurrence_end_date": {
                        "type": "string",
                        "format": "date",
                        "description": "End date for the recurrence in YYYY-MM-DD format"
                    },
                    "recurrence_interval": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Interval for the recurrence (e.g., every 2 weeks)"
                    }
                },
                "required": ["task_id", "recurrence_pattern"]
            }
        }
    }