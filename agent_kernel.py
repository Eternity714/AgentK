from dotenv import load_dotenv
load_dotenv()

from agents import hermes
from uuid import uuid4

def main():
    """AgentK主入口，支持streaming模式"""
    uuid = str(uuid4())
    
    print("🚀 欢迎使用AgentK - 自主进化的AGI系统")
    print("💡 现在支持实时streaming输出，您可以看到AI的思考过程！")
    print("="*60)
    
    # 启动Hermes with streaming
    hermes.hermes(uuid, streaming=True)

if __name__ == "__main__":
    main()