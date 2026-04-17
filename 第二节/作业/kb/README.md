# AI 知识库助手 - GitHub API 工具

## 概述

这是 AI 知识库助手项目的一部分，提供了从 GitHub API 获取仓库基本信息的 Python 工具函数。

## 功能特性

- ✅ 获取指定仓库的 Star 数、Fork 数、描述等基本信息
- ✅ 支持从 GitHub URL 直接获取仓库信息
- ✅ 批量获取多个仓库信息
- ✅ 检查 GitHub API 调用限制
- ✅ 支持 GitHub Token 认证（提高 API 限制）
- ✅ 完整的错误处理和日志记录
- ✅ 类型提示和 Google 风格文档注释

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 基本用法

```python
from utils.github_api import get_repo_info

# 获取单个仓库信息
repo_info = get_repo_info("openai", "openai-python")
print(f"Star数: {repo_info['stars']}")
print(f"Fork数: {repo_info['forks']}")
print(f"描述: {repo_info['description']}")
```

### 从 URL 获取

```python
from utils.github_api import get_repo_info_from_url

repo_info = get_repo_info_from_url("https://github.com/langchain-ai/langchain")
print(f"仓库: {repo_info['full_name']}")
print(f"Star数: {repo_info['stars']}")
```

### 批量获取

```python
from utils.github_api import get_multiple_repos_info

repos = [
    "facebook/react",
    "tensorflow/tensorflow",
    "microsoft/vscode"
]

results = get_multiple_repos_info(repos)
for repo_info in results:
    print(f"{repo_info['full_name']}: {repo_info['stars']} stars")
```

### 检查 API 限制

```python
from utils.github_api import check_rate_limit

rate_info = check_rate_limit()
print(f"剩余调用次数: {rate_info['remaining']}/{rate_info['limit']}")
```

### 使用 GitHub Token

1. 创建 `.env` 文件：
```bash
cp .env.example .env
```

2. 在 `.env` 文件中设置你的 GitHub Token：
```env
GITHUB_TOKEN=your_github_personal_access_token_here
```

3. 在代码中使用：
```python
import os
from dotenv import load_dotenv
from utils.github_api import get_repo_info

load_dotenv()
github_token = os.getenv("GITHUB_TOKEN")

repo_info = get_repo_info("openai", "openai-python", github_token=github_token)
```

## API 文档

### `get_repo_info(repo_owner, repo_name, github_token=None)`

获取指定仓库的基本信息。

**参数:**
- `repo_owner` (str): 仓库所有者（用户名或组织名）
- `repo_name` (str): 仓库名称
- `github_token` (str, optional): GitHub 个人访问令牌

**返回:**
包含仓库信息的字典，包括：
- `stars`: Star 数
- `forks`: Fork 数  
- `description`: 仓库描述
- `language`: 主要编程语言
- `created_at`: 创建时间
- `updated_at`: 最后更新时间
- 等更多字段...

### `get_repo_info_from_url(repo_url, github_token=None)`

从 GitHub URL 获取仓库信息。

### `get_multiple_repos_info(repo_list, github_token=None)`

批量获取多个仓库的信息。

### `check_rate_limit(github_token=None)`

检查 GitHub API 调用限制。

## 运行示例

```bash
# 运行内置测试
python utils/github_api.py

# 运行使用示例
python example_usage.py
```

## 错误处理

函数会抛出以下异常：
- `requests.exceptions.RequestException`: 网络请求错误
- `ValueError`: 仓库不存在或参数错误
- `KeyError`: 解析响应数据失败

建议使用 try-except 块捕获异常：

```python
try:
    repo_info = get_repo_info("openai", "openai-python")
except ValueError as e:
    print(f"仓库不存在: {e}")
except requests.exceptions.RequestException as e:
    print(f"网络错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

## 注意事项

1. 未认证的 API 调用限制为 60 次/小时
2. 使用 GitHub Token 可将限制提高到 5000 次/小时
3. 建议在需要大量调用时配置 GitHub Token
4. 所有网络请求都有 10 秒超时设置
5. 遵循项目的编码规范（PEP 8, Google docstring 等）

## 集成到 AI 知识库项目

这个模块可以直接集成到 AGENTS.md 中定义的采集器（collector）中，用于获取 GitHub Trending 中 AI/LLM 项目的详细信息。

## 许可证

遵循项目的统一许可证。