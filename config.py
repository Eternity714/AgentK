import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# 加载环境变量
load_dotenv()

# 从环境变量读取配置
default_model_temperature = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
default_model_provider = os.getenv("MODEL_PROVIDER", "OPENAI").upper()
default_model_name = os.getenv("MODEL_NAME", "gpt-4o")
default_api_key = os.getenv("MODEL_API_KEY")
default_base_url = os.getenv("MODEL_BASE_URL")

# 根据提供商创建模型实例
match default_model_provider:
    case "OPENAI":
        if default_base_url:
            # 自定义OpenAI兼容API
            default_langchain_model = ChatOpenAI(
                model=default_model_name,
                temperature=default_model_temperature,
                api_key=default_api_key,
                base_url=default_base_url
            )
        else:
            # 标准OpenAI API
            default_langchain_model = ChatOpenAI(
                model=default_model_name,
                temperature=default_model_temperature,
                api_key=default_api_key or os.getenv("OPENAI_API_KEY")
            )
    case "ANTHROPIC":
        default_langchain_model = ChatAnthropic(
            model=default_model_name,
            temperature=default_model_temperature,
            api_key=default_api_key or os.getenv("ANTHROPIC_API_KEY")
        )
    case "OLLAMA":
        default_langchain_model = ChatOpenAI(
            model=default_model_name,
            temperature=default_model_temperature,
            api_key="ollama",  # Ollama不需要真实API key
            base_url=default_base_url or "http://localhost:11434/v1"
        )
    case _:
        raise ValueError(f"不支持的模型提供商: {default_model_provider}")

def get_model():
    """获取默认的语言模型实例"""
    return default_langchain_model

def get_model_config():
    """获取模型配置信息"""
    return {
        "provider": default_model_provider,
        "model_name": default_model_name,
        "temperature": default_model_temperature,
        "base_url": default_base_url
    }
