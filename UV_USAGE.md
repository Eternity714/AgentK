# UV 使用指南

本项目已迁移到使用 `uv` 进行依赖管理。以下是完整的使用指南：

## 🚀 快速开始

### 1. 项目初始化
```bash
# 安装依赖并初始化项目
uv sync

# 检查项目状态
uv run python check_project.py

# 启动AgentK
uv run python start.py
# 或者直接运行
uv run python agent_kernel.py
```

### 2. 环境配置
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入你的API密钥
# 支持OpenAI、Anthropic、Ollama等多种模型提供商
```

## 安装依赖

```bash
# 安装所有依赖（包括开发依赖）
uv sync

# 仅安装生产依赖
uv sync --no-dev
```

## 运行项目

```bash
# 在虚拟环境中运行 Python 脚本
uv run python agent_kernel.py

# 或者激活虚拟环境后运行
uv shell
python agent_kernel.py
```

## 添加新依赖

```bash
# 添加生产依赖
uv add package_name

# 添加开发依赖
uv add --dev package_name

# 添加特定版本
uv add "package_name==1.0.0"
```

## 移除依赖

```bash
# 移除依赖
uv remove package_name
```

## 更新依赖

```bash
# 更新所有依赖
uv lock --upgrade

# 更新特定依赖
uv lock --upgrade-package package_name
```

## 运行测试

```bash
# 运行测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov
```

## 代码格式化和检查

```bash
# 格式化代码
uv run black .

# 代码风格检查
uv run flake8 .

# 类型检查
uv run mypy .
```

## 项目结构

- `pyproject.toml` - 项目配置和依赖定义
- `uv.lock` - 锁定的依赖版本（自动生成）
- `.venv/` - 虚拟环境目录（自动创建）

## 迁移说明

原来的 `requirements.txt` 文件已被 `pyproject.toml` 替代。所有依赖现在都在 `pyproject.toml` 中管理。

注意：由于网络问题，暂时移除了 `unstructured` 依赖。如需使用，可以稍后手动添加：

```bash
uv add unstructured
```