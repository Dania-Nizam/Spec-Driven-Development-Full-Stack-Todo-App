"""
MCP (Model Context Protocol) Server for Todo Chatbot Integration

This module implements the Model Context Protocol server using the official SDK that exposes
standardized tools for todo operations with JWT authentication and stateful conversation support.
"""
import os
import logging
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.api.dependencies.auth import get_current_user_id
from .config import MCPConfig
from .auth import verify_jwt_token
from .session import SessionManager
from .context import ConversationContextManager
from .registry import ToolRegistry
from .models import MCPServerHealthResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
config = MCPConfig()
session_manager = SessionManager(config.session_timeout)
context_manager = ConversationContextManager()
tool_registry = ToolRegistry()

# Initialize FastAPI app
app = FastAPI(
    title="Todo Chatbot MCP Server",
    description="Model Context Protocol server for standardized todo operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom middleware for MCP protocol headers
@app.middleware("http")
async def mcp_protocol_middleware(request, call_next):
    """
    Middleware to handle MCP protocol negotiation and headers.
    Ensures proper MCP protocol compliance.
    """
    # Add MCP protocol headers to responses
    response = await call_next(request)

    # Set standard MCP headers
    response.headers["X-MCP-Version"] = "1.0.0"
    response.headers["X-MCP-Protocol"] = "model-context-protocol"
    response.headers["X-Server-Name"] = "Todo Chatbot MCP Server"

    # Add content-type header for MCP responses
    if request.url.path.startswith('/mcp/') or request.url.path in ['/capabilities', '/.well-known/mcp-capabilities']:
        response.headers["Content-Type"] = "application/json; charset=utf-8"

    return response


@app.get("/health")
async def health_check():
    """Health check endpoint for the MCP server."""
    return MCPServerHealthResponse(
        status="healthy",
        service="mcp-server",
        version="1.0.0",
        timestamp=datetime.utcnow()
    ).dict()


@app.get("/.well-known/mcp-capabilities")
@app.get("/mcp/capabilities")
async def get_capabilities():
    """
    MCP capabilities endpoint that returns server capabilities
    conforming to the Model Context Protocol specification.
    """
    capabilities_response = {
        "deprecated": {
            "tools": {
                "version": "1.0.0"
            }
        },
        "prompts": {
            "version": "1.0.0"
        },
        "resources": {
            "version": "1.0.0"
        },
        "server_info": {
            "name": "Todo Chatbot MCP Server",
            "version": "1.0.0"
        }
    }
    return capabilities_response


# Protocol negotiation endpoint
@app.get("/.well-known/meta.protocol")
async def protocol_negotiation():
    """
    MCP protocol negotiation endpoint following the Model Context Protocol specification.
    This endpoint provides information about the server's supported protocols and versions.
    """
    # Check for incoming MCP-Version header
    # This is typically handled by FastAPI middleware but we return protocol info

    return {
        "mcp_version": "1.0.0",
        "supported_protocols": ["model-context-protocol"],
        "endpoints": {
            "capabilities": "/.well-known/mcp-capabilities",
            "resources": "/resources",
            "prompts": "/prompts",
            "tools": "/mcp/tools"
        },
        "server": {
            "name": "Todo Chatbot MCP Server",
            "version": "1.0.0",
            "description": "MCP server for todo operations with context management"
        "backend.mcp.server.py"

    }


@app.get("/mcp/tools/list")
async def list_tools(
    authenticated_user_id: int = Depends(get_current_user_id)
):
    """
    List all available MCP tools.

    Args:
        authenticated_user_id: The authenticated user ID from JWT token

    Returns:
        A list of available tools with their schemas
    """
    # Verify user authentication
    if authenticated_user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid JWT token")

    # Return registered tools
    tools_list = tool_registry.get_available_tools()
    return {"tools": tools_list}


@app.post("/mcp/tools/{tool_name}")
async def execute_tool(
    tool_name: str,
    tool_params: Dict[str, Any],
    background_tasks: BackgroundTasks,
    authenticated_user_id: int = Depends(get_current_user_id)
):
    """
    Execute a specific MCP tool with provided parameters.

    Args:
        tool_name: The name of the tool to execute
        tool_params: Parameters to pass to the tool
        background_tasks: FastAPI background tasks handler
        authenticated_user_id: The authenticated user ID from JWT token

    Returns:
        Result of the tool execution
    """
    # Verify user authentication
    if authenticated_user_id is None:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "error": "unauthorized",
                "message": "Invalid or missing JWT token",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    # Verify that the tool exists
    if not tool_registry.is_tool_registered(tool_name):
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": "tool_not_found",
                "message": f"Tool '{tool_name}' is not available",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    try:
        # Create or retrieve session
        session_id = tool_params.get("session_id")
        if not session_id:
            session_id = session_manager.create_session(authenticated_user_id)

        # Validate session
        session = session_manager.validate_session(session_id, authenticated_user_id)
        if not session:
            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "error": "session_expired",
                    "message": "Session has expired or is invalid",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

        # Execute the tool
        result = await tool_registry.execute_tool(
            tool_name=tool_name,
            user_id=authenticated_user_id,
            params=tool_params,
            session_id=session_id
        )

        # Update session activity
        session_manager.update_session_activity(session_id)

        # Return successful result
        return {
            "success": True,
            "result": result,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "server_error",
                "message": f"Internal server error while executing tool: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@app.get("/mcp/session/{session_id}")
async def get_session(
    session_id: str,
    authenticated_user_id: int = Depends(get_current_user_id)
):
    """
    Get information about a specific MCP session.

    Args:
        session_id: The ID of the session to retrieve
        authenticated_user_id: The authenticated user ID from JWT token

    Returns:
        Session information with context summary
    """
    # Verify user authentication
    if authenticated_user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid JWT token")

    # Get session information
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": "not_found",
                "message": f"Session '{session_id}' not found",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    # Verify user owns the session
    if session["user_id"] != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "error": "forbidden",
                "message": "Access denied: You can only access your own sessions",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    # Get context information
    context = context_manager.get_context(session_id)

    return {
        "session_id": session["session_id"],
        "user_id": session["user_id"],
        "created_at": session["created_at"],
        "last_activity_at": session["last_activity_at"],
        "expires_at": session["expires_at"],
        "is_active": session["is_active"],
        "context_summary": {
            "previous_tasks_referenced": context.get("previous_tasks_referenced", []),
            "current_topic": context.get("current_topic", ""),
            "pending_clarifications": context.get("pending_clarifications", [])
        }
    }


# Initialize tools when the application starts
@app.on_event('startup')
async def startup_event():
    """Initialize the MCP server and register all tools."""
    logger.info("Starting MCP server with official SDK compatibility...")

    # Register all available tools with the registry
    from .tools.add_task import add_task_tool
    from .tools.view_tasks import view_tasks_tool
    from .tools.update_task import update_task_tool
    from .tools.delete_task import delete_task_tool
    from .tools.mark_complete import mark_complete_tool
    from .tools.search_filter_tasks import search_filter_tasks_tool
    from .tools.set_recurring import set_recurring_tool
    from .tools.get_task_context import get_task_context_tool

    # Register tools with the registry
    tool_registry.register_tool("add_task", add_task_tool)
    tool_registry.register_tool("view_tasks", view_tasks_tool)
    tool_registry.register_tool("update_task", update_task_tool)
    tool_registry.register_tool("delete_task", delete_task_tool)
    tool_registry.register_tool("mark_complete", mark_complete_tool)
    tool_registry.register_tool("search_filter_tasks", search_filter_tasks_tool)
    tool_registry.register_tool("set_recurring", set_recurring_tool)
    tool_registry.register_tool("get_task_context", get_task_context_tool)

    logger.info("MCP server initialized with all tools using official SDK compatibility")


# MCP-specific endpoints following the protocol specification
@app.get("/resources")
async def get_resources():
    """
    MCP Resources endpoint - lists available resources that can be accessed
    following the Model Context Protocol specification.
    """
    # Return a list of available resources
    resources = [
        {
            "uri": "todo://tasks",
            "name": "User Tasks",
            "description": "Current user's todo tasks"
        },
        {
            "uri": "todo://contexts",
            "name": "Conversation Contexts",
            "description": "Current conversation contexts and history"
        }
    ]
    return {"resources": resources}


@app.get("/resources/{resource_id}")
async def get_resource(resource_id: str):
    """
    MCP Resource endpoint - gets a specific resource
    following the Model Context Protocol specification.
    """
    # Handle specific resource requests
    if resource_id == "tasks":
        # This would return the current user's tasks
        return {"resource": {"type": "tasks", "data": []}}
    elif resource_id == "contexts":
        # This would return the current context
        return {"resource": {"type": "contexts", "data": {}}}
    else:
        raise HTTPException(status_code=404, detail=f"Resource {resource_id} not found")


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "mcp.server:app",
        host=config.host,
        port=config.port,
        reload=config.debug
    )