from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
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

# 创建ReAct代理
agent = create_react_agent(
    model=config.default_langchain_model,
    tools=tools,
    prompt=system_prompt
)

def software_engineer(task: str) -> str:
    """Creates, modifies, and deletes code, manages files, runs shell commands, and collaborates with other agents."""
    result = agent.invoke(
        {"messages": [HumanMessage(task)]}
    )
    return result