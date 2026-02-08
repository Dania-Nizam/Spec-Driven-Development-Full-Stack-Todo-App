"""Registry of all agent skills for the todo chatbot."""

from .add_task_skill.add_task_skill import add_task_skill, get_openai_tool_definition as get_add_task_tool
from .delete_task_skill.delete_task_skill import delete_task_skill, get_openai_tool_definition as get_delete_task_tool
from .update_task_skill.update_task_skill import update_task_skill, get_openai_tool_definition as get_update_task_tool
from .view_tasks_skill.view_tasks_skill import view_tasks_skill, get_openai_tool_definition as get_view_tasks_tool
from .mark_complete_skill.mark_complete_skill import mark_complete_skill, get_openai_tool_definition as get_mark_complete_tool
from .search_filter_tasks_skill.search_filter_tasks_skill import search_filter_tasks_skill, get_openai_tool_definition as get_search_filter_tool
from .set_recurring_skill.set_recurring_skill import set_recurring_skill, get_openai_tool_definition as get_set_recurring_tool
from .auth_check_skill.auth_check_skill import auth_check_skill, get_openai_tool_definition as get_auth_check_tool
from .get_task_context_skill.get_task_context_skill import get_task_context_skill, get_openai_tool_definition as get_task_context_tool

# All skill functions
ALL_SKILLS = {
    'add_task_skill': add_task_skill,
    'delete_task_skill': delete_task_skill,
    'update_task_skill': update_task_skill,
    'view_tasks_skill': view_tasks_skill,
    'mark_complete_skill': mark_complete_skill,
    'search_filter_tasks_skill': search_filter_tasks_skill,
    'set_recurring_skill': set_recurring_skill,
    'auth_check_skill': auth_check_skill,
    'get_task_context_skill': get_task_context_skill,
}

# All OpenAI tool definitions
ALL_TOOL_DEFINITIONS = [
    get_add_task_tool(),
    get_delete_task_tool(),
    get_update_task_tool(),
    get_view_tasks_tool(),
    get_mark_complete_tool(),
    get_search_filter_tool(),
    get_set_recurring_tool(),
    get_auth_check_tool(),
    get_task_context_tool(),
]

def get_skill(name: str):
    """Get a specific skill by name."""
    return ALL_SKILLS.get(name)

def get_all_skills():
    """Get all available skills."""
    return ALL_SKILLS

def get_all_tool_definitions():
    """Get all OpenAI tool definitions."""
    return ALL_TOOL_DEFINITIONS

__all__ = [
    'add_task_skill',
    'delete_task_skill',
    'update_task_skill',
    'view_tasks_skill',
    'mark_complete_skill',
    'search_filter_tasks_skill',
    'set_recurring_skill',
    'auth_check_skill',
    'get_task_context_skill',
    'ALL_SKILLS',
    'ALL_TOOL_DEFINITIONS',
    'get_skill',
    'get_all_skills',
    'get_all_tool_definitions'
]