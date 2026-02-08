"""Skill to mark a todo task as complete or incomplete."""

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


def mark_complete_skill(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Marks a todo task as complete or incomplete via the backend API with JWT authentication.

    Args:
        params: Dictionary containing task ID and completion status
                - task_id (str, required): The ID of the task to update
                - complete (bool, required): Whether to mark as complete (True) or incomplete (False)

    Returns:
        Dict with success status and message
    """
    try:
        task_id = params.get('task_id')
        complete = params.get('complete')

        if not task_id:
            return {"success": False, "message": "task_id is required"}

        if complete is None:
            return {"success": False, "message": "complete status is required (True/False)"}

        # Get user_id from JWT token context (simplified for this example)
        user_id = "1"  # This should come from decoded JWT

        # Determine the status based on the complete flag
        new_status = "completed" if complete else "pending"

        # Prepare update payload
        update_data = {"status": new_status}

        # Make API call to update the task status
        headers = {
            "Authorization": f"Bearer {BETTER_AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"{BACKEND_BASE_URL}/api/{user_id}/tasks/{task_id}"

        response = httpx.patch(url, json=update_data, headers=headers)

        status_text = "completed" if complete else "marked as incomplete"
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Task with ID '{task_id}' {status_text} successfully"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "message": f"Task with ID '{task_id}' not found"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to update task status: {response.text}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating task status: {str(e)}"
        }


# Register the function with OpenAI
def get_openai_tool_definition():
    """Returns the OpenAI tool definition for this skill."""
    return {
        "type": "function",
        "function": {
            "name": "mark_complete_skill",
            "description": "Marks a todo task as complete or incomplete",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update"
                    },
                    "complete": {
                        "type": "boolean",
                        "description": "Whether to mark the task as complete (True) or incomplete (False)"
                    }
                },
                "required": ["task_id", "complete"]
            }
        }
    }