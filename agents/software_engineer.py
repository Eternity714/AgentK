from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

import config

system_prompt = """你是software_engineer，一个能够创建、修改和删除代码的ReAct代理。

你拥有管理文件、运行shell命令以及通过分配任务与其他代理协作的工具。
"""

from tools.write_to_file import write_to_file
from tools.overwrite_file import overwrite_file
from tools.delete_file import delete_file
from tools.read_file import read_file
from tools.run_shell_command import run_shell_command
from tools.assign_agent_to_task import assign_agent_to_task
from tools.list_available_agents import list_available_agents

tools = [
    write_to_file,
    overwrite_file,
    delete_file,
    read_file,
    run_shell_command,
    assign_agent_to_task,
    list_available_agents
]

def reasoning(state: MessagesState):
    print("software_engineer is thinking...")
    messages = state['messages']
    tooled_up_model = config.default_langchain_model.bind_tools(tools)
    response = tooled_up_model.invoke(messages)
    return {"messages": [response]}

def check_for_tool_calls(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    
    if last_message.tool_calls:
        if not last_message.content.strip() == "":
            print("software_engineer thought this:")
            print(last_message.content)
        print()
        print("software_engineer is acting by invoking these tools:")
        print([tool_call["name"] for tool_call in last_message.tool_calls])
        return "tools"
    
    return END

acting = ToolNode(tools)

workflow = StateGraph(MessagesState)
workflow.add_node("reasoning", reasoning)
workflow.add_node("tools", acting)
workflow.set_entry_point("reasoning")
workflow.add_conditional_edges(
    "reasoning",
    check_for_tool_calls,
)
workflow.add_edge("tools", 'reasoning')

graph = workflow.compile()


def software_engineer(task: str) -> str:
    """Creates, modifies, and deletes code, manages files, runs shell commands, and collaborates with other agents."""
    return graph.invoke(
        {"messages": [SystemMessage(system_prompt), HumanMessage(task)]}
    )