from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
import config
import utils

system_prompt = """你是web_researcher，一个能够使用网络研究答案的ReAct代理。

你拥有搜索网络的工具和获取网页内容的工具。
"""
    
from tools.duck_duck_go_web_search import duck_duck_go_web_search
from tools.fetch_web_page_content import fetch_web_page_content

tools = [duck_duck_go_web_search, fetch_web_page_content]

# 创建ReAct代理
agent = create_react_agent(
    model=config.default_langchain_model,
    tools=tools,
    prompt=system_prompt
)

def web_researcher(task: str, streaming: bool = True) -> str:
    """Researches the web."""
    if streaming:
        return web_researcher_stream(task)
    else:
        result = agent.invoke(
            {"messages": [HumanMessage(task)]}
        )
        return result

def web_researcher_stream(task: str) -> str:
    """Web Researcher的streaming模式实现"""
    return utils.agent_stream(agent, task, "Web Researcher", "🌐")