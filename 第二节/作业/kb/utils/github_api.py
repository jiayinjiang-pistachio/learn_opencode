"""
GitHub API 工具函数模块
提供从GitHub API获取仓库基本信息的函数
"""

import logging
import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin

# 设置日志
logger = logging.getLogger(__name__)

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
        包含仓库信息的字典，格式为：
        {
            "stars": int,           # Star数
            "forks": int,           # Fork数
            "description": str,     # 仓库描述
            "language": str,        # 主要编程语言
            "created_at": str,      # 创建时间
            "updated_at": str,      # 最后更新时间
            "homepage": str,        # 项目主页
            "topics": list[str],    # 标签主题
            "owner": str,           # 所有者
            "name": str,            # 仓库名
            "full_name": str,       # 完整仓库名（owner/name）
            "html_url": str,        # GitHub页面URL
            "open_issues": int,     # 打开的issue数
            "watchers": int,        # 观察者数
            "default_branch": str   # 默认分支
        }

    Raises:
        requests.exceptions.RequestException: 网络请求错误
        ValueError: 仓库不存在或参数错误
    """
    # 构建API URL
    api_url = urljoin(GITHUB_API_BASE, f"/repos/{repo_owner}/{repo_name}")

    logger.info(f"获取仓库信息: {repo_owner}/{repo_name}")

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

        # 提取关键信息
        repo_info = {
            "stars": repo_data.get("stargazers_count", 0),
            "forks": repo_data.get("forks_count", 0),
            "description": repo_data.get("description", ""),
            "language": repo_data.get("language", ""),
            "created_at": repo_data.get("created_at", ""),
            "updated_at": repo_data.get("updated_at", ""),
            "homepage": repo_data.get("homepage", ""),
            "topics": repo_data.get("topics", []),
            "owner": repo_data.get("owner", {}).get("login", repo_owner),
            "name": repo_data.get("name", repo_name),
            "full_name": repo_data.get("full_name", f"{repo_owner}/{repo_name}"),
            "html_url": repo_data.get("html_url", ""),
            "open_issues": repo_data.get("open_issues_count", 0),
            "watchers": repo_data.get("watchers_count", 0),
            "default_branch": repo_data.get("default_branch", "main"),
            "license": repo_data.get("license", {}).get("name", "")
            if repo_data.get("license")
            else "",
        }

        logger.info(
            f"成功获取仓库信息: {repo_info['full_name']} - {repo_info['stars']} stars"
        )
        return repo_info

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            error_msg = f"仓库不存在: {repo_owner}/{repo_name}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e
        elif response.status_code == 403:
            error_msg = "API调用次数限制，请使用GitHub Token或稍后重试"
            logger.error(error_msg)
            raise requests.exceptions.RequestException(error_msg) from e
        else:
            error_msg = f"GitHub API请求失败: {e}"
            logger.error(error_msg)
            raise
    except requests.exceptions.RequestException as e:
        error_msg = f"网络请求错误: {e}"
        logger.error(error_msg)
        raise
    except (KeyError, ValueError) as e:
        error_msg = f"解析响应数据失败: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg) from e


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


def get_multiple_repos_info(
    repo_list: list, github_token: Optional[str] = None
) -> list[Dict[str, Any]]:
    """
    批量获取多个仓库的信息

    Args:
        repo_list: 仓库列表，每个元素可以是：
                   - 字符串格式 "owner/repo"
                   - 字典格式 {"owner": "owner", "repo": "repo"}
                   - 完整的GitHub URL
        github_token: GitHub个人访问令牌（可选）

    Returns:
        仓库信息列表，按照输入顺序排列
    """
    results = []

    for repo_item in repo_list:
        try:
            if isinstance(repo_item, dict):
                owner = repo_item.get("owner")
                repo = repo_item.get("repo")
                if owner and repo:
                    repo_info = get_repo_info(owner, repo, github_token)
                else:
                    logger.warning(f"跳过无效的仓库字典: {repo_item}")
                    continue
            elif isinstance(repo_item, str):
                if "/" in repo_item and not repo_item.startswith("http"):
                    # 格式: owner/repo
                    parts = repo_item.split("/")
                    if len(parts) >= 2:
                        owner, repo = parts[0], parts[1]
                        repo_info = get_repo_info(owner, repo, github_token)
                    else:
                        logger.warning(f"跳过无效的仓库字符串: {repo_item}")
                        continue
                elif repo_item.startswith("https://github.com/"):
                    # GitHub URL
                    repo_info = get_repo_info_from_url(repo_item, github_token)
                else:
                    logger.warning(f"跳过无法识别的仓库格式: {repo_item}")
                    continue
            else:
                logger.warning(f"跳过无法处理的仓库类型: {type(repo_item)}")
                continue

            results.append(repo_info)

        except Exception as e:
            logger.error(f"获取仓库信息失败: {repo_item}, 错误: {e}")
            # 添加错误信息，保持结果顺序
            results.append({"error": str(e), "input": str(repo_item)})

    return results


def check_rate_limit(github_token: Optional[str] = None) -> Dict[str, Any]:
    """
    检查GitHub API调用限制

    Args:
        github_token: GitHub个人访问令牌（可选）

    Returns:
        包含API限制信息的字典
    """
    api_url = urljoin(GITHUB_API_BASE, "/rate_limit")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-Knowledge-Base-Agent",
    }

    if github_token:
        headers["Authorization"] = f"token {github_token}"

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()

        rate_data = response.json()
        resources = rate_data.get("resources", {})
        core_limit = resources.get("core", {})

        rate_info = {
            "limit": core_limit.get("limit", 60),
            "remaining": core_limit.get("remaining", 60),
            "used": core_limit.get("used", 0),
            "reset_timestamp": core_limit.get("reset", 0),
            "is_authenticated": github_token is not None,
        }

        logger.info(f"API限制: {rate_info['remaining']}/{rate_info['limit']} 剩余")
        return rate_info

    except requests.exceptions.RequestException as e:
        logger.error(f"检查API限制失败: {e}")
        raise


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 测试示例
    try:
        # 测试获取仓库信息
        print("测试获取 openai/openai-python 仓库信息:")
        info = get_repo_info("openai", "openai-python")
        print(f"Star数: {info['stars']}")
        print(f"Fork数: {info['forks']}")
        print(f"描述: {info['description']}")
        print(f"语言: {info['language']}")

        print("\n" + "=" * 50 + "\n")

        # 测试从URL获取
        print("测试从URL获取 langchain-ai/langchain 仓库信息:")
        url_info = get_repo_info_from_url("https://github.com/langchain-ai/langchain")
        print(f"Star数: {url_info['stars']}")
        print(f"描述: {url_info['description']}")

        print("\n" + "=" * 50 + "\n")

        # 测试批量获取
        print("测试批量获取多个仓库信息:")
        repos = [
            "facebook/react",
            "https://github.com/tensorflow/tensorflow",
            {"owner": "microsoft", "repo": "vscode"},
        ]

        batch_info = get_multiple_repos_info(repos)
        for i, repo_info in enumerate(batch_info):
            if "error" in repo_info:
                print(f"仓库 {repos[i]} 获取失败: {repo_info['error']}")
            else:
                print(f"{repo_info['full_name']}: {repo_info['stars']} stars")

        print("\n" + "=" * 50 + "\n")

        # 测试API限制
        print("测试API限制检查:")
        rate_info = check_rate_limit()
        print(f"剩余调用次数: {rate_info['remaining']}/{rate_info['limit']}")

    except Exception as e:
        print(f"测试失败: {e}")
