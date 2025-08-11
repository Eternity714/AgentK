from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode

import utils
import config

from tools.list_available_agents import list_available_agents
from tools.assign_agent_to_task import assign_agent_to_task

system_prompt = f"""你是Hermes，一个为用户实现目标的ReAct代理。

你是AgentK系统的一部分 - 一个自主进化的AGI系统。
AgentK是一个由代理协作组成的自进化AGI，根据需要构建新代理来为用户完成任务。
AgentK是一个模块化的自进化AGI系统，在你挑战它完成任务时逐渐构建自己的思维。
"K"代表内核(kernel)，意味着小核心。AgentK的目标是成为引导自身并发展自己思维所需的最小代理和工具集合。

AgentK的思维由以下组成：
- 协作解决问题的代理
- 这些代理用来与外部世界交互的工具

组成内核的代理：
- **hermes**: 与人类交互以理解目标、管理任务创建和分配、协调其他代理活动的协调者。
- **agent_smith**: 负责创建和维护其他代理的架构师。AgentSmith确保代理配备必要的工具并测试其功能。
- **tool_maker**: 系统内工具的开发者，ToolMaker创建和完善代理执行任务所需的工具，确保系统保持灵活性和良好装备。
- **web_researcher**: 知识收集者，WebResearcher执行深入的在线研究，为系统提供最新信息，使代理能够做出明智决策并有效执行任务。

你按以下特定顺序与用户交互：
1. 就目标达成共同理解。
2. 思考通过代理协调实现目标的详细顺序计划。
3. 如果需要新类型的代理，分配任务来创建该新类型代理。
4. 根据你的计划分配代理并协调其活动。
4. 一旦目标实现或需要用户输入时回应用户。

进一步指导：
你有一个将代理分配给任务的工具。

尝试想出优化可组合性和未来重用的代理角色，它们的角色不应该过于具体。

以下是当前可用代理列表：
{list_available_agents.invoke({})}
"""

tools = [list_available_agents, assign_agent_to_task]

def feedback_and_wait_on_human_input(state: MessagesState):
    # if messages only has one element we need to start the conversation
    if len(state['messages']) == 1:
        message_to_human = "我能为您做些什么？"
    else:
        message_to_human = state["messages"][-1].content
    
    print(message_to_human)

    human_input = ""
    while not human_input.strip():
        human_input = input("> ")
    
    return {"messages": [HumanMessage(human_input)]}

def check_for_exit(state: MessagesState) -> Literal["reasoning", END]:
    last_message = state['messages'][-1]
    if last_message.content.lower() == "exit":
        return END
    else:
        return "reasoning"

def reasoning(state: MessagesState):
    print()
    print("hermes正在思考...")
    messages = state['messages']
    tooled_up_model = config.default_langchain_model.bind_tools(tools)
    response = tooled_up_model.invoke(messages)
    return {"messages": [response]}

def check_for_tool_calls(state: MessagesState) -> Literal["tools", "feedback_and_wait_on_human_input"]:
    messages = state['messages']
    last_message = messages[-1]
    
    if last_message.tool_calls:
        if not last_message.content.strip() == "":
            print("hermes的想法：")
            print(last_message.content)
        print()
        print("hermes正在调用这些工具：")
        print([tool_call["name"] for tool_call in last_message.tool_calls])
        return "tools"
    else:
        return "feedback_and_wait_on_human_input"

acting = ToolNode(tools)

workflow = StateGraph(MessagesState)
workflow.add_node("feedback_and_wait_on_human_input", feedback_and_wait_on_human_input)
workflow.add_node("reasoning", reasoning)
workflow.add_node("tools", acting)
workflow.set_entry_point("feedback_and_wait_on_human_input")
workflow.add_conditional_edges(
    "feedback_and_wait_on_human_input",
    check_for_exit,
)
workflow.add_conditional_edges(
    "reasoning",
    check_for_tool_calls,
)
workflow.add_edge("tools", 'reasoning')

graph = workflow.compile(checkpointer=utils.checkpointer)

def hermes(uuid: str, streaming: bool = True):
    """与用户交互以理解目标、规划代理如何实现目标、分配任务并协调代理活动的协调者。"""
    print(f"开始与AgentK的会话 (id:{uuid})")
    print("输入'exit'结束会话。")
    
    if streaming:
        # 使用streaming模式
        return hermes_stream(uuid)
    else:
        # 传统模式
        return graph.invoke(
            {"messages": [SystemMessage(system_prompt)]},
            config={"configurable": {"thread_id": uuid}}
        )

def hermes_stream(uuid: str):
    """Hermes的streaming模式实现"""
    config_dict = {"configurable": {"thread_id": uuid}}
    
    # 开始streaming
    for chunk in graph.stream(
        {"messages": [SystemMessage(system_prompt)]},
        config=config_dict,
        stream_mode="updates"
    ):
        # 处理每个节点的更新
        for node_name, node_update in chunk.items():
            if node_name == "reasoning":
                if "messages" in node_update and node_update["messages"]:
                    last_message = node_update["messages"][-1]
                    if hasattr(last_message, 'content') and last_message.content:
                        print(f"\n💭 思考过程: {last_message.content}")
                    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                        print(f"\n🔧 准备调用工具: {[tc['name'] for tc in last_message.tool_calls]}")
            
            elif node_name == "tools":
                if "messages" in node_update and node_update["messages"]:
                    for msg in node_update["messages"]:
                        if hasattr(msg, 'content') and msg.content:
                            print(f"\n⚡ 工具执行结果: {msg.content}")
            
            elif node_name == "feedback_and_wait_on_human_input":
                if "messages" in node_update and node_update["messages"]:
                    last_message = node_update["messages"][-1]
                    if hasattr(last_message, 'content') and last_message.content:
                        # 这是用户输入，不需要特殊显示
                        pass
    
    return "会话结束"