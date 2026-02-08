"""Skill to delete a todo task."""

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


def delete_task_skill(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deletes a todo task via the backend API with JWT authentication.

    Args:
        params: Dictionary containing deletion criteria
                - task_id (str, optional): The ID of the task to delete
                - title (str, optional): The title of the task to delete

    Returns:
        Dict with success status and message
    """
    try:
        task_id = params.get('task_id')
        title = params.get('title')

        if not task_id and not title:
            return {"success": False, "message": "Either task_id or title is required"}

        # Get user_id from JWT token context (simplified for this example)
        user_id = "1"  # This should come from decoded JWT

        # If only title is provided, find the task ID first
        if not task_id and title:
            # Search for the task by title
            headers = {
                "Authorization": f"Bearer {BETTER_AUTH_TOKEN}",
                "Content-Type": "application/json"
            }

            search_url = f"{BACKEND_BASE_URL}/api/{user_id}/tasks/search"
            search_payload = {"query": title}

            search_response = httpx.post(search_url, json=search_payload, headers=headers)

            if search_response.status_code == 200:
                search_results = search_response.json()
                if search_results and len(search_results) > 0:
                    task_id = search_results[0]['id']
                else:
                    return {"success": False, "message": f"No task found with title '{title}'"}
            else:
                return {"success": False, "message": f"Failed to search for task: {search_response.text}"}

        # Make API call to delete the task
        headers = {
            "Authorization": f"Bearer {BETTER_AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"{BACKEND_BASE_URL}/api/{user_id}/tasks/{task_id}"

        response = httpx.delete(url, headers=headers)

        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Task with ID '{task_id}' deleted successfully"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "message": f"Task with ID '{task_id}' not found"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to delete task: {response.text}"
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting task: {str(e)}"
        }


# Register the function with OpenAI
def get_openai_tool_definition():
    """Returns the OpenAI tool definition for this skill."""
    return {
        "type": "function",
        "function": {
            "name": "delete_task_skill",
            "description": "Deletes a todo task from the user's task list",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to delete"
                    },
                    "title": {
                        "type": "string",
                        "description": "The title of the task to delete (used if ID not provided)"
                    }
                },
                "anyOf": [
                    {"required": ["task_id"]},
                    {"required": ["title"]}
                ]
            }
        }
    }