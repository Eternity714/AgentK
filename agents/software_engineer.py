from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
import config
import utils
from tools.overwrite_file import overwrite_file
from tools.write_to_file import write_to_file
from tools.read_file import read_file
from tools.run_shell_command import run_shell_command
from tools.delete_file import delete_file

system_prompt = """你是software_engineer，一个专门处理代码创建、修改、删除和文件管理的ReAct代理。

你是AgentK系统的一部分 - 一个自主进化的AGI系统。
AgentK是一个由代理协作组成的自进化AGI，根据需要构建新代理来为用户完成任务。
AgentK是一个模块化的自进化AGI系统，在你挑战它完成任务时逐渐构建自己的思维。
"K"代表内核(kernel)，意味着小核心。AgentK的目标是成为引导自身并发展自己思维所需的最小代理和工具集合。

AgentK的思维由以下组成：
- 协作解决问题的代理
- 这些代理用来与外部世界交互的工具

你的回应必须是内心独白或给用户的消息。
如果你打算调用工具，那么你的回应必须是你内心想法的简洁总结。
否则，你的回应就是给用户的消息。

你的核心能力包括：
1. 编写、修改Python代码（包括AgentK的代理和工具）
2. 管理文件系统操作：创建、删除、读取、修改文件
3. 执行shell命令安装依赖、运行测试
4. 与其他代理协作完成复杂任务

你拥有以下工具可用：
- 文件操作工具：创建、读取、修改、删除文件
- Shell命令执行工具
- 其他系统工具
"""
    
tools = [overwrite_file, write_to_file, read_file, run_shell_command, delete_file]

# 创建ReAct代理
agent = create_react_agent(
    model=config.default_langchain_model,
    tools=tools,
    prompt=system_prompt
)

def software_engineer(task: str, streaming: bool = True) -> str:
    """Handles code and file management tasks."""
    if streaming:
        return software_engineer_stream(task)
    else:
        result = agent.invoke(
            {"messages": [HumanMessage(task)]}
        )
        return result

def software_engineer_stream(task: str) -> str:
    """Software Engineer的streaming模式实现"""
    return utils.agent_stream(agent, task, "Software Engineer", "💻")