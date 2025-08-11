import importlib.util
import os
import re
import sys
from typing import List, Optional
from langchain_core.messages import HumanMessage

def load_module(module_path: str):
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_code_blocks(text: str) -> List[str]:
    pattern = r"```(?:python)?\n(.*?)```"
    return re.findall(pattern, text, re.DOTALL)

def extract_tool_code(text: str) -> str:
    code_blocks = get_code_blocks(text)
    return code_blocks[0].strip() if code_blocks else ""

def get_agent(agent_name: str):
    if "utils" in sys.modules:
        del sys.modules["utils"]
    agent_path = os.path.join("agents", f"{agent_name}.py")
    if not os.path.exists(agent_path):
        raise ValueError(f"Agent {agent_name} not found at {agent_path}")
    agent_module = load_module(agent_path)
    return getattr(agent_module, agent_name)

def agent_stream(agent, task: str, agent_name: str, emoji: str) -> str:
    """通用的agent streaming函数"""
    print(f"\n{emoji} {agent_name} 开始处理任务: {task}")
    print("="*60)
    
    # 使用streaming模式
    for chunk in agent.stream(
        {"messages": [HumanMessage(task)]},
        stream_mode="updates"
    ):
        # 处理每个节点的更新
        for node_name, node_update in chunk.items():
            if node_name == "agent":
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
    
    print("\n" + "="*60)
    print(f"✅ {agent_name} 任务完成")
    return "任务处理完成"
