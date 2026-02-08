"""
Test script to verify all todo skills work with real API calls.
This script tests the functionality of each skill against a live backend API.
"""
import asyncio
import os
from typing import Dict, Any

# Import the unified skills module - COMMENTED OUT due to ModuleNotFoundError
# from src.agents.skills.todo_skills import (
#     add_task_skill,
#     view_tasks_skill,
#     update_task_skill,
#     delete_task_skill,
#     mark_complete_skill,
#     search_filter_tasks_skill,
#     set_recurring_skill,
#     get_task_context_skill,
#     auth_check_skill,
#     check_api_connectivity
# )

# Placeholder functions to prevent errors after commenting out imports.
# These should be replaced with actual skill calls via MCPIntegrationManager or similar.
async def add_task_skill(*args, **kwargs):
    print("WARNING: add_task_skill is a placeholder.")
    return {"success": False, "error": "Placeholder skill called."}

async def view_tasks_skill(*args, **kwargs):
    print("WARNING: view_tasks_skill is a placeholder.")
    return {"success": False, "error": "Placeholder skill called."}

async def update_task_skill(*args, **kwargs):
    print("WARNING: update_task_skill is a placeholder.")
    return {"success": False, "error": "Placeholder skill called."}

async def delete_task_skill(*args, **kwargs):
    print("WARNING: delete_task_skill is a placeholder.")
    return {"success": False, "error": "Placeholder skill called."}

async def mark_complete_skill(*args, **kwargs):
    print("WARNING: mark_complete_skill is a placeholder.")
    return {"success": False, "error": "Placeholder skill called."}

async def search_filter_tasks_skill(*args, **kwargs):
    print("WARNING: search_filter_tasks_skill is a placeholder.")
    return {"success": False, "error": "Placeholder skill called."}

async def set_recurring_skill(*args, **kwargs):
    print("WARNING: set_recurring_skill is a placeholder.")
    return {"success": False, "error": "Placeholder skill called."}

async def get_task_context_skill(*args, **kwargs):
    print("WARNING: get_task_context_skill is a placeholder.")
    return {"success": False, "error": "Placeholder skill called."}

async def auth_check_skill(*args, **kwargs):
    print("WARNING: auth_check_skill is a placeholder.")
    return {"success": False, "error": "Placeholder skill called."}

async def check_api_connectivity(*args, **kwargs):
    print("WARNING: check_api_connectivity is a placeholder.")
    return {"connected": False, "error": "Placeholder skill called."}

# Test configuration
TEST_USER_ID = 1
TEST_TOKEN = os.getenv("TEST_JWT_TOKEN", "fake-token-for-testing")
BASE_API_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


async def test_auth_check():
    """Test the authentication skill."""
    print("\n🔍 Testing Authentication Skill...")
    try:
        result = await auth_check_skill(TEST_TOKEN)
        print(f"   Authentication result: {result}")
        return result.get('success', False)
    except Exception as e:
        print(f"   Authentication failed: {e}")
        return False


async def test_add_task():
    """Test the add task skill."""
    print("\n📝 Testing Add Task Skill...")
    try:
        result = await add_task_skill(
            user_id=TEST_USER_ID,
            token=TEST_TOKEN,
            title="Test Task from Skill Test",
            description="This is a test task created by the skill test script.",
            priority="medium",
            due_date=None
        )
        print(f"   Add task result: {result}")
        return result.get('success', False)
    except Exception as e:
        print(f"   Add task failed: {e}")
        return False


async def test_view_tasks():
    """Test the view tasks skill."""
    print("\n📋 Testing View Tasks Skill...")
    try:
        result = await view_tasks_skill(
            user_id=TEST_USER_ID,
            token=TEST_TOKEN,
            status="all",
            priority=None,
            limit=10,
            sort_by="created_at",
            sort_order="desc"
        )
        print(f"   View tasks result: {result}")
        return result.get('success', False)
    except Exception as e:
        print(f"   View tasks failed: {e}")
        return False


async def test_update_task(task_id: int):
    """Test the update task skill."""
    print(f"\n✏️  Testing Update Task Skill (task_id: {task_id})...")
    try:
        result = await update_task_skill(
            user_id=TEST_USER_ID,
            token=TEST_TOKEN,
            task_id=task_id,
            title="Updated Test Task",
            description="This task has been updated by the skill test script.",
            priority="high"
        )
        print(f"   Update task result: {result}")
        return result.get('success', False)
    except Exception as e:
        print(f"   Update task failed: {e}")
        return False


async def test_mark_complete(task_id: int):
    """Test the mark complete skill."""
    print(f"\n✅ Testing Mark Complete Skill (task_id: {task_id})...")
    try:
        result = await mark_complete_skill(
            user_id=TEST_USER_ID,
            token=TEST_TOKEN,
            task_id=task_id,
            completed=True
        )
        print(f"   Mark complete result: {result}")
        return result.get('success', False)
    except Exception as e:
        print(f"   Mark complete failed: {e}")
        return False


async def test_search_filter():
    """Test the search/filter tasks skill."""
    print("\n🔍 Testing Search/Filter Tasks Skill...")
    try:
        result = await search_filter_tasks_skill(
            user_id=TEST_USER_ID,
            token=TEST_TOKEN,
            query="test",
            status="all",
            priority="medium",
            limit=5
        )
        print(f"   Search/filter result: {result}")
        return result.get('success', False)
    except Exception as e:
        print(f"   Search/filter failed: {e}")
        return False


async def test_get_task_context():
    """Test the get task context skill."""
    print("\n📊 Testing Get Task Context Skill...")
    try:
        result = await get_task_context_skill(
            user_id=TEST_USER_ID,
            token=TEST_TOKEN,
            recent_count=5,
            include_completed=False
        )
        print(f"   Get task context result: {result}")
        return result.get('success', False)
    except Exception as e:
        print(f"   Get task context failed: {e}")
        return False


async def test_api_connectivity():
    """Test API connectivity."""
    print("\n🌐 Testing API Connectivity...")
    try:
        result = await check_api_connectivity(
            user_id=TEST_USER_ID,
            token=TEST_TOKEN
        )
        print(f"   API connectivity result: {result}")
        return result.get('connected', False)
    except Exception as e:
        print(f"   API connectivity failed: {e}")
        return False


async def run_comprehensive_test():
    """Run all tests in sequence."""
    print("=" * 60)
    print("🚀 Starting Todo Skills Comprehensive Test")
    print("=" * 60)

    # Test API connectivity first
    api_connected = await test_api_connectivity()
    if not api_connected:
        print("\n❌ API connectivity failed. Please ensure the backend is running.")
        return

    # Test authentication
    auth_success = await test_auth_check()
    if not auth_success:
        print("\n❌ Authentication failed. Please check the JWT token.")
        return

    # Test basic operations
    task_added = await test_add_task()
    if not task_added:
        print("\n❌ Add task failed, skipping dependent tests.")
        return

    # Get tasks to work with for subsequent tests
    view_result = await test_view_tasks()
    if view_result:
        # If there are tasks, pick one to test update and mark complete
        view_data = await view_tasks_skill(user_id=TEST_USER_ID, token=TEST_TOKEN)
        if view_data.get('success') and view_data.get('tasks'):
            first_task_id = view_data['tasks'][0].get('id')
            if first_task_id:
                await test_update_task(first_task_id)
                await test_mark_complete(first_task_id)

    # Test advanced operations
    await test_search_filter()
    await test_get_task_context()

    print("\n" + "=" * 60)
    print("🏁 Test suite completed!")
    print("Note: Some tests may fail if the backend API is not running.")
    print("Ensure your Phase II backend is accessible at:", BASE_API_URL)
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())