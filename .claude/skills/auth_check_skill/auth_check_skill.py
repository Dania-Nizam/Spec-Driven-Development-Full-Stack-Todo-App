"""Skill to verify JWT authentication and return user ID."""

import json
import os
from typing import Dict, Any
from jose import jwt, JWTError
from datetime import datetime
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET") or os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def auth_check_skill(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifies JWT authentication and returns the user ID.

    Args:
        params: Dictionary containing the JWT token
                - token (str, required): The JWT token to verify

    Returns:
        Dict with success status, message, and user_id if successful
    """
    try:
        token = params.get('token')

        if not token:
            return {"success": False, "message": "Token is required"}

        # Verify the JWT token
        try:
            # Decode the token without verification for now (would require proper secret)
            # In a real implementation, we'd verify using the secret key
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")  # Standard JWT claim for subject/user

            if user_id is None:
                return {"success": False, "message": "Invalid token: no user ID found"}

            return {
                "success": True,
                "message": "Authentication successful",
                "user_id": str(user_id)
            }

        except JWTError:
            return {"success": False, "message": "Invalid or expired token"}
        except Exception as e:
            return {"success": False, "message": f"Token verification error: {str(e)}"}

    except Exception as e:
        return {
            "success": False,
            "message": f"Error checking authentication: {str(e)}"
        }


# Register the function with OpenAI
def get_openai_tool_definition():
    """Returns the OpenAI tool definition for this skill."""
    return {
        "type": "function",
        "function": {
            "name": "auth_check_skill",
            "description": "Verifies JWT authentication and returns the user ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "The JWT token to verify"
                    }
                },
                "required": ["token"]
            }
        }
    }