#!/usr/bin/env python3
"""
AgentK 项目状态检查脚本
用于验证项目初始化是否成功
"""

import os
import sys
from pathlib import Path

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"  ✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查.env文件
    if Path(".env").exists():
        print("  ✅ .env文件存在")
    else:
        print("  ❌ .env文件不存在")
        return False
    
    # 检查数据库文件
    if Path("checkpoints.sqlite").exists():
        print("  ✅ checkpoints.sqlite数据库文件存在")
    else:
        print("  ❌ checkpoints.sqlite数据库文件不存在")
        return False
    
    return True

def check_dependencies():
    """检查依赖包"""
    print("\n📦 检查核心依赖...")
    
    required_packages = [
        "langgraph",
        "langchain_community",
        "langchain_openai",
        "langchain_anthropic",
        "selenium",
        "duckduckgo_search",
        "dotenv",
        "aiosqlite"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - 未安装")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_config():
    """检查配置模块"""
    print("\n⚙️ 检查配置模块...")
    
    try:
        import config
        print("  ✅ config.py模块加载成功")
        
        # 检查模型配置
        if hasattr(config, 'get_model'):
            print("  ✅ get_model函数存在")
        else:
            print("  ❌ get_model函数不存在")
            return False
            
        return True
    except Exception as e:
        print(f"  ❌ 配置模块加载失败: {e}")
        return False

def check_agents():
    """检查代理模块"""
    print("\n🤖 检查代理模块...")
    
    agents = [
        "agents.agent_smith",
        "agents.software_engineer", 
        "agents.web_researcher",
        "agents.tool_maker"
    ]
    
    failed_agents = []
    
    for agent in agents:
        try:
            __import__(agent)
            print(f"  ✅ {agent}")
        except Exception as e:
            print(f"  ❌ {agent} - 加载失败: {e}")
            failed_agents.append(agent)
    
    return len(failed_agents) == 0

def check_tools():
    """检查工具模块"""
    print("\n🔧 检查工具模块...")
    
    try:
        import utils
        tools = utils.all_tool_functions()
        
        if isinstance(tools, dict):
            print(f"  ✅ 成功加载 {len(tools)} 个工具")
            # 显示可用工具
            for tool_name in sorted(tools.keys()):
                print(f"    - {tool_name}")
        elif isinstance(tools, list):
            print(f"  ✅ 成功加载 {len(tools)} 个工具")
            # 显示可用工具
            for i, tool in enumerate(tools):
                tool_name = getattr(tool, '__name__', f'tool_{i}')
                print(f"    - {tool_name}")
        else:
            print(f"  ⚠️ 工具加载返回了意外的类型: {type(tools)}")
            
        return True
    except Exception as e:
        print(f"  ❌ 工具模块加载失败: {e}")
        return False

def main():
    """主检查函数"""
    print("🚀 AgentK 项目状态检查")
    print("=" * 50)
    
    checks = [
        ("环境配置", check_environment),
        ("依赖包", check_dependencies),
        ("配置模块", check_config),
        ("代理模块", check_agents),
        ("工具模块", check_tools)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ {check_name}检查时发生错误: {e}")
            results.append((check_name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 检查结果总结:")
    
    all_passed = True
    for check_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {check_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查通过！项目已成功初始化。")
        print("\n💡 你现在可以运行以下命令启动AgentK:")
        print("   uv run python agent_kernel.py")
    else:
        print("⚠️ 部分检查失败，请检查上述错误信息。")
        print("\n💡 建议运行以下命令重新安装依赖:")
        print("   uv sync")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)