#!/usr/bin/env python3
"""
AgentK 启动脚本
简化的启动入口，自动检查环境并启动AgentK
"""

import os
import sys
from pathlib import Path

def check_environment():
    """快速环境检查"""
    print("🔍 检查环境...")
    
    # 检查.env文件
    if not Path(".env").exists():
        print("❌ .env文件不存在，请先配置环境变量")
        print("💡 可以复制.env.example为.env并填入你的API密钥")
        return False
    
    # 检查数据库文件
    if not Path("checkpoints.sqlite").exists():
        print("⚠️ 数据库文件不存在，正在创建...")
        import sqlite3
        conn = sqlite3.connect('checkpoints.sqlite')
        conn.close()
        print("✅ 数据库文件已创建")
    
    return True

def main():
    """主启动函数"""
    print("🚀 AgentK 启动中...")
    print("=" * 40)
    
    # 环境检查
    if not check_environment():
        sys.exit(1)
    
    print("✅ 环境检查通过")
    print("🤖 正在启动AgentK...")
    print("=" * 40)
    
    # 导入并启动AgentK
    try:
        import agent_kernel
        # agent_kernel.py会自动运行主程序
    except KeyboardInterrupt:
        print("\n👋 AgentK已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("\n💡 请检查配置或运行以下命令进行诊断:")
        print("   uv run python check_project.py")
        sys.exit(1)

if __name__ == "__main__":
    main()