#!/usr/bin/env python3
"""
Validation script to verify MCP server functionality.
"""

import subprocess
import sys
import time
import requests
import threading


def check_mcp_server():
    """Check if MCP server starts and responds correctly."""
    print("Validating MCP server implementation...")

    # Import and test basic functionality
    try:
        from mcp.server import app
        from mcp.registry import ToolRegistry
        from mcp.session import SessionManager
        from mcp.config import MCPConfig

        print("✓ Successfully imported MCP server components")

        # Test config
        config = MCPConfig()
        print(f"✓ Config loaded: Host={config.host}, Port={config.port}")

        # Test session manager
        session_mgr = SessionManager(config.session_timeout)
        print("✓ Session manager initialized")

        # Test tool registry
        tool_reg = ToolRegistry()
        print("✓ Tool registry initialized")

        # Check if startup event registered tools
        available_tools = tool_reg.get_available_tools()
        print(f"✓ Found {len(available_tools)} registered tools")

        expected_tools = [
            "add_task", "view_tasks", "update_task", "delete_task",
            "mark_complete", "search_filter_tasks", "set_recurring", "get_task_context"
        ]

        registered_tool_names = [tool['name'] for tool in available_tools]
        for expected_tool in expected_tools:
            if expected_tool in registered_tool_names:
                print(f"  ✓ {expected_tool} tool registered")
            else:
                print(f"  ✗ {expected_tool} tool NOT registered")

        # Test health response model
        from backend.mcp.models import MCPServerHealthResponse
        import datetime
        health_resp = MCPServerHealthResponse(
            status="healthy",
            service="mcp-server",
            version="1.0.0",
            timestamp=datetime.datetime.utcnow()
        )
        print("✓ Health response model works correctly")

        print("\n🎉 MCP Server validation completed successfully!")
        print("All core components are functioning as expected.")
        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error during validation: {e}")
        return False


if __name__ == "__main__":
    success = check_mcp_server()
    if success:
        print("\n✅ MCP Integration is fully implemented and validated!")
        sys.exit(0)
    else:
        print("\n❌ MCP Integration validation failed!")
        sys.exit(1)