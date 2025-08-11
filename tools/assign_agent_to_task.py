import sys
from utils import get_agent

def assign_agent_to_task(agent_name: str, task: str) -> str:
    """Assigns a task to a specific agent and returns the result."""
    try:
        agent_function = get_agent(agent_name)
        result = agent_function(task=task)
        # Handle both structured messages and raw string responses
        if isinstance(result, dict) and "messages" in result:
            return result["messages"][-1].content
        else:
            return str(result)
    except Exception as e:
        return f"Error assigning task to {agent_name}: {str(e)}"
