"""Skill to search and filter todo tasks."""

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


def search_filter_tasks_skill(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Searches and filters the user's todo tasks via the backend API with JWT authentication.

    Args:
        params: Dictionary containing search and filter criteria
                - query (str, optional): Search term to match in task titles or descriptions
                - filter_status (str, optional): Filter by status (pending, in_progress, completed)
                - filter_priority (str, optional): Filter by priority (low, medium, high)
                - filter_due_date_from (str, optional): Filter tasks with due date on or after YYYY-MM-DD
                - filter_due_date_to (str, optional): Filter tasks with due date on or before YYYY-MM-DD
                - tags (list, optional): Filter tasks by tags
                - sort_by (str, optional): Sort by field (title, due_date, priority, created_at)
                - order (str, optional): Sort order (asc, desc)

    Returns:
        Dict with success status, message, and tasks array
    """
    try:
        # Get user_id from JWT token context (simplified for this example)
        user_id = "1"  # This should come from decoded JWT

        # Build query parameters
        query_params = {}
        if params.get('query'):
            query_params['query'] = params['query']
        if params.get('filter_status'):
            query_params['status'] = params['filter_status']
        if params.get('filter_priority'):
            query_params['priority'] = params['filter_priority']
        if params.get('filter_due_date_from'):
            query_params['due_date_from'] = params['filter_due_date_from']
        if params.get('filter_due_date_to'):
            query_params['due_date_to'] = params['filter_due_date_to']
        if params.get('tags'):
            query_params['tags'] = ','.join(params['tags'])
        if params.get('sort_by'):
            query_params['sort_by'] = params['sort_by']
        if params.get('order'):
            query_params['order'] = params['order']

        # Make API call to search and filter tasks
        headers = {
            "Authorization": f"Bearer {BETTER_AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"{BACKEND_BASE_URL}/api/{user_id}/tasks/search"

        # Add query parameters to the URL
        if query_params:
            query_string = "&".join([f"{k}={v}" for k, v in query_params.items()])
            url += f"?{query_string}"

        response = httpx.get(url, headers=headers)

        if response.status_code == 200:
            tasks = response.json()
            return {
                "success": True,
                "message": f"Found {len(tasks)} matching tasks",
                "tasks": tasks
            }
        else:
            return {
                "success": False,
                "message": f"Failed to search/filter tasks: {response.text}",
                "tasks": []
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error searching/filtering tasks: {str(e)}",
            "tasks": []
        }


# Register the function with OpenAI
def get_openai_tool_definition():
    """Returns the OpenAI tool definition for this skill."""
    return {
        "type": "function",
        "function": {
            "name": "search_filter_tasks_skill",
            "description": "Searches and filters the user's todo tasks",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term to match in task titles or descriptions"
                    },
                    "filter_status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed"],
                        "description": "Filter tasks by status"
                    },
                    "filter_priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Filter tasks by priority"
                    },
                    "filter_due_date_from": {
                        "type": "string",
                        "format": "date",
                        "description": "Filter tasks with due date on or after YYYY-MM-DD"
                    },
                    "filter_due_date_to": {
                        "type": "string",
                        "format": "date",
                        "description": "Filter tasks with due date on or before YYYY-MM-DD"
                    },
                    "tags": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Filter tasks by tags"
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["title", "due_date", "priority", "created_at"],
                        "description": "Sort tasks by field"
                    },
                    "order": {
                        "type": "string",
                        "enum": ["asc", "desc"],
                        "description": "Sort order (ascending or descending)"
                    }
                }
            }
        }
    }