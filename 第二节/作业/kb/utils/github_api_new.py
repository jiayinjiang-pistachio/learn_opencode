"""
GitHub API 工具函数模块
简化版本：从GitHub API获取指定仓库的基本信息
"""

import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin

# GitHub API 基础URL
GITHUB_API_BASE = "https://api.github.com"


def get_repo_info(
    repo_owner: str, repo_name: str, github_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    从GitHub API获取指定仓库的基本信息

    Args:
        repo_owner: 仓库所有者（用户名或组织名）
        repo_name: 仓库名称
        github_token: GitHub个人访问令牌（可选，用于提高API调用限制）

    Returns:
        包含仓库信息的字典，包含：
        {
            "stars": int,           # Star数
            "forks": int,           # Fork数
            "description": str,     # 仓库描述
            "full_name": str,       # 完整仓库名（owner/name）
            "html_url": str         # GitHub页面URL
        }

    Raises:
        requests.exceptions.RequestException: 网络请求错误
        ValueError: 仓库不存在或参数错误
    """
    # 构建API URL
    api_url = urljoin(GITHUB_API_BASE, f"/repos/{repo_owner}/{repo_name}")

    # 准备请求头
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-Knowledge-Base-Agent",
    }

    # 如果提供了token，添加到请求头
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()

        repo_data = response.json()

        # 提取关键信息：Star数、Fork数、描述
        repo_info = {
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "description": repo_data.get("description", ""),
            "full_name": repo_data.get("full_name", f"{repo_owner}/{repo_name}"),
            "html_url": repo_data.get("html_url", ""),
        }

        return repo_info

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ValueError(f"仓库不存在: {repo_owner}/{repo_name}") from e
        elif response.status_code == 403:
            raise requests.exceptions.RequestException(
                "API调用次数限制，请使用GitHub Token或稍后重试"
            ) from e
        else:
            raise
    except requests.exceptions.RequestException as e:
        raise
    except (KeyError, ValueError) as e:
        raise ValueError(f"解析响应数据失败: {e}") from e


def get_repo_info_from_url(
    repo_url: str, github_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    从GitHub URL获取仓库信息

    Args:
        repo_url: GitHub仓库URL，例如: https://github.com/owner/repo
        github_token: GitHub个人访问令牌（可选）

    Returns:
        包含仓库信息的字典

    Raises:
        ValueError: URL格式错误
    """
    # 从URL中提取owner和repo
    if not repo_url.startswith("https://github.com/"):
        raise ValueError(f"无效的GitHub URL: {repo_url}")

    # 移除末尾的.git（如果有）
    repo_url = repo_url.rstrip(".git")

    # 分割URL获取owner和repo
    parts = repo_url.split("/")
    if len(parts) < 5:
        raise ValueError(f"无法从URL提取仓库信息: {repo_url}")

    repo_owner = parts[3]
    repo_name = parts[4]

    return get_repo_info(repo_owner, repo_name, github_token)


if __name__ == "__main__":
    # 测试示例
    try:
        # 测试获取仓库信息
        print("测试获取 openai/openai-python 仓库信息:")
        info = get_repo_info("openai", "openai-python")
        print(f"仓库名: {info['full_name']}")
        print(f"URL: {info['html_url']}")
        print(f"Star数: {info['stars']}")
        print(f"Fork数: {info['forks']}")
        print(f"描述: {info['description']}")

        print("\n" + "=" * 50 + "\n")

        # 测试从URL获取
        print("测试从URL获取 langchain-ai/langchain 仓库信息:")
        url_info = get_repo_info_from_url("https://github.com/langchain-ai/langchain")
        print(f"仓库名: {url_info['full_name']}")
        print(f"Star数: {url_info['stars']}")
        print(f"Fork数: {url_info['forks']}")
        print(f"描述: {url_info['description']}")

    except Exception as e:
        print(f"测试失败: {e}")
