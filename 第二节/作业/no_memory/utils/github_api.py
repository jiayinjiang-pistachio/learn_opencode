import requests
import json
from typing import Dict, Optional
from datetime import datetime


def get_repo_info(owner: str, repo: str, token: Optional[str] = None) -> Dict:
    """
    获取GitHub仓库的基本信息

    Args:
        owner: 仓库所有者（用户名或组织名）
        repo: 仓库名称
        token: GitHub API token（可选，用于提高速率限制）

    Returns:
        包含仓库信息的字典，包括：
        - name: 仓库名称
        - full_name: 仓库完整名称
        - description: 仓库描述
        - stars: Star数
        - forks: Fork数
        - watchers: Watch数
        - open_issues: 未关闭的issue数
        - language: 主要编程语言
        - created_at: 创建时间
        - updated_at: 更新时间
        - pushed_at: 最后推送时间
        - html_url: GitHub页面URL
        - clone_url: 克隆URL
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Repo-Info-Fetcher",
    }

    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        return {
            "name": data.get("name", ""),
            "full_name": data.get("full_name", ""),
            "description": data.get("description", ""),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "watchers": data.get("watchers_count", 0),
            "open_issues": data.get("open_issues_count", 0),
            "language": data.get("language", ""),
            "created_at": data.get("created_at", ""),
            "updated_at": data.get("updated_at", ""),
            "pushed_at": data.get("pushed_at", ""),
            "html_url": data.get("html_url", ""),
            "clone_url": data.get("clone_url", ""),
            "license": data.get("license", {}).get("name", "")
            if data.get("license")
            else "",
            "size": data.get("size", 0),
            "default_branch": data.get("default_branch", "main"),
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": f"请求失败: {str(e)}",
            "status_code": response.status_code if "response" in locals() else None,
        }
    except json.JSONDecodeError as e:
        return {"error": f"JSON解析失败: {str(e)}"}


def save_repo_info_to_file(repo_info: Dict, filename: str = "repo_info.json") -> bool:
    """
    将仓库信息保存到JSON文件

    Args:
        repo_info: 仓库信息字典
        filename: 保存的文件名

    Returns:
        bool: 保存是否成功
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(repo_info, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"保存文件失败: {e}")
        return False


def format_repo_info(repo_info: Dict) -> str:
    """
    格式化仓库信息为可读字符串

    Args:
        repo_info: 仓库信息字典

    Returns:
        格式化后的字符串
    """
    if "error" in repo_info:
        return f"错误: {repo_info['error']}"

    output = []
    output.append(f"仓库: {repo_info.get('full_name', 'N/A')}")
    output.append(f"描述: {repo_info.get('description', '无描述')}")
    output.append(f"⭐ Stars: {repo_info.get('stars', 0):,}")
    output.append(f"🍴 Forks: {repo_info.get('forks', 0):,}")
    output.append(f"👁️ Watchers: {repo_info.get('watchers', 0):,}")
    output.append(f"🐛 未关闭Issues: {repo_info.get('open_issues', 0):,}")
    output.append(f"主要语言: {repo_info.get('language', '未知')}")
    output.append(f"许可证: {repo_info.get('license', '无')}")
    output.append(f"默认分支: {repo_info.get('default_branch', 'main')}")
    output.append(f"创建时间: {repo_info.get('created_at', '未知')}")
    output.append(f"最后更新: {repo_info.get('updated_at', '未知')}")
    output.append(f"GitHub页面: {repo_info.get('html_url', '')}")

    return "\n".join(output)


if __name__ == "__main__":
    # 示例用法
    print("获取GitHub仓库信息示例")
    print("=" * 50)

    # 测试获取opencode仓库信息
    repo_info = get_repo_info("anomalyco", "opencode")

    if "error" not in repo_info:
        print(format_repo_info(repo_info))

        # 保存到文件
        if save_repo_info_to_file(repo_info, "opencode_info.json"):
            print("\n✅ 信息已保存到 opencode_info.json")
    else:
        print(f"获取失败: {repo_info['error']}")

    print("\n" + "=" * 50)
    print("使用示例:")
    print("1. 获取仓库信息: repo_info = get_repo_info('owner', 'repo')")
    print("2. 格式化输出: print(format_repo_info(repo_info))")
    print("3. 保存到文件: save_repo_info_to_file(repo_info, 'output.json')")
