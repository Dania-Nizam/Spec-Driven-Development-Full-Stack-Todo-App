"""
Simple chatbot orchestrator for processing natural language todo commands.
"""
import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime


class SimpleChatbotOrchestrator:
    """
    Simple orchestrator that parses user messages and calls appropriate MCP tools.
    """

    def __init__(self):
        self.intent_patterns = {
            "add_task": [
                r"add\s+(?:a\s+)?task\s+(.+)",
                r"create\s+(?:a\s+)?task\s+(.+)",
                r"new\s+task\s+(.+)",
                r"remind\s+me\s+to\s+(.+)",
                r"i\s+need\s+to\s+(.+)",
                r"todo\s+(.+)",
                r"make\s+(?:a\s+)?task\s+(.+)",
            ],
            "view_tasks": [
                r"show\s+(?:me\s+)?(?:my\s+)?(?:all\s+)?tasks?(?:\s+list)?",
                r"list\s+(?:all\s+)?(?:my\s+)?tasks?",
                r"what\s+(?:are\s+)?(?:my\s+)?tasks?",
                r"view\s+(?:my\s+)?tasks?",
                r"get\s+(?:my\s+)?tasks?",
                r"see\s+(?:my\s+)?tasks?",
                r"display\s+tasks?",
                r"tasks?\s+list",
            ],
            "delete_task": [
                r"dele?t[e]?\s+task\s+(?:#)?(\d+)",  # Handles "delet", "delete"
                r"remove\s+task\s+(?:#)?(\d+)",
                r"cancel\s+task\s+(?:#)?(\d+)",
                r"del\s+task\s+(?:#)?(\d+)",
                r"erase\s+task\s+(?:#)?(\d+)",
            ],
            "mark_complete": [
                r"complete\s+task\s+(?:#)?(\d+)",
                r"finish\s+task\s+(?:#)?(\d+)",
                r"done\s+(?:with\s+)?task\s+(?:#)?(\d+)",
                r"mark\s+task\s+(?:#)?(\d+)\s+(?:as\s+)?(?:complete|done)",
                r"task\s+(?:#)?(\d+)\s+(?:is\s+)?done",
                r"check\s+(?:off\s+)?task\s+(?:#)?(\d+)",
            ],
            "update_task": [
                r"update\s+task\s+(?:#)?(\d+)\s+(?:to\s+)?(.+)",
                r"change\s+task\s+(?:#)?(\d+)\s+(?:to\s+)?(.+)",
                r"edit\s+task\s+(?:#)?(\d+)\s+(?:to\s+)?(.+)",
                r"modify\s+task\s+(?:#)?(\d+)\s+(?:to\s+)?(.+)",
                r"rename\s+task\s+(?:#)?(\d+)\s+(?:to\s+)?(.+)",
            ],
            "user_info": [
                r"who\s+am\s+i",
                r"my\s+info",
                r"user\s+info",
                r"my\s+profile",
                r"who\s+is\s+logged\s+in",
                r"what\s+is\s+my\s+(?:name|id)",
            ],
        }

    def detect_intent(self, message: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """
        Detect user intent from message using pattern matching.

        Returns:
            Tuple of (intent_name, extracted_params)
        """
        message_lower = message.lower().strip()

        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message_lower)
                if match:
                    params = {}

                    if intent == "add_task":
                        params["title"] = match.group(1).strip()
                        params["description"] = None
                        params["priority"] = "medium"

                    elif intent in ["delete_task", "mark_complete"]:
                        params["task_id"] = int(match.group(1))

                    elif intent == "update_task":
                        params["task_id"] = int(match.group(1))
                        params["title"] = match.group(2).strip()

                    return intent, params

        return None, None

    async def process_message(
        self,
        user_id: int,
        message: str,
        session_id: str,
        orchestrator_adapter
    ) -> Dict[str, Any]:
        """
        Process a user message and execute the appropriate action.

        Args:
            user_id: The authenticated user ID
            message: The user's message
            session_id: The session ID
            orchestrator_adapter: The MCP orchestrator adapter

        Returns:
            Dict with response, success status, and conversation context
        """
        # Detect intent
        intent, params = self.detect_intent(message)

        if not intent:
            return {
                "message": "میں سمجھ نہیں پایا۔ آپ یہ کمانڈز استعمال کر سکتے ہیں:\n"
                          "- 'add task Buy groceries' - نیا ٹاسک بنانے کے لیے\n"
                          "- 'show my tasks' - اپنے ٹاسک دیکھنے کے لیے\n"
                          "- 'complete task 1' - ٹاسک مکمل کرنے کے لیے\n"
                          "- 'delete task 2' - ٹاسک ڈیلیٹ کرنے کے لیے\n"
                          "- 'update task 1 New title' - ٹاسک اپڈیٹ کرنے کے لیے\n"
                          "- 'who am i' - اپنی معلومات دیکھنے کے لیے",
                "success": True,
                "conversation_context": {"last_intent": "unknown"}
            }

        # Handle user info request (no MCP tool needed)
        if intent == "user_info":
            return {
                "message": f"آپ User ID {user_id} کے ساتھ لاگ ان ہیں",
                "success": True,
                "conversation_context": {"last_intent": "user_info"}
            }

        # Execute MCP tool based on intent
        try:
            result = await orchestrator_adapter.call_mcp_tool(
                tool_name=intent,
                user_id=user_id,
                params=params,
                session_id=session_id
            )

            if result.get("success"):
                response_message = self._format_success_response(intent, result, params)
            else:
                response_message = f"معذرت، یہ کام نہیں ہو سکا۔ خرابی: {result.get('error', 'Unknown error')}"

            return {
                "message": response_message,
                "success": result.get("success", False),
                "conversation_context": {
                    "last_intent": intent,
                    "last_action": result.get("message", ""),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }

        except Exception as e:
            return {
                "message": f"ایک خرابی ہوئی: {str(e)}",
                "success": False,
                "conversation_context": {"last_intent": intent, "error": str(e)}
            }

    def _format_success_response(self, intent: str, result: Dict[str, Any], params: Dict[str, Any]) -> str:
        """Format a user-friendly success response based on the intent."""

        if intent == "add_task":
            task_title = params.get("title", "your task")
            return f"✅ ٹاسک شامل ہو گیا: '{task_title}'"

        elif intent == "view_tasks":
            # Fixed: tasks are at top level, not nested in "result"
            tasks = result.get("tasks", [])
            if not tasks:
                return "ابھی آپ کے پاس کوئی ٹاسک نہیں ہے۔ 'add task [تفصیل]' سے نیا ٹاسک بنائیں"

            task_list = "\n".join([
                f"#{task['id']}: {task['title']} {'✓' if task.get('completed') else '○'}"
                for task in tasks[:10]  # Limit to 10 tasks
            ])
            total = result.get("total_count", len(tasks))
            return f"📋 آپ کے ٹاسک (کل {total}):\n{task_list}"

        elif intent == "delete_task":
            task_id = params.get("task_id")
            return f"🗑️ ٹاسک #{task_id} ڈیلیٹ ہو گیا"

        elif intent == "mark_complete":
            task_id = params.get("task_id")
            return f"✅ ٹاسک #{task_id} مکمل ہو گیا!"

        elif intent == "update_task":
            task_id = params.get("task_id")
            new_title = params.get("title", "")
            return f"✏️ ٹاسک #{task_id} اپڈیٹ ہو گیا: '{new_title}'"

        return result.get("message", "کام مکمل ہو گیا")
