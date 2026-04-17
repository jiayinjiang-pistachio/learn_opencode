"""
使用 utils/github_api.py 的示例
"""

import logging
from utils.github_api import (
    get_repo_info,
    get_repo_info_from_url,
    get_multiple_repos_info,
    check_rate_limit,
)

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    """示例用法"""

    print("=== GitHub API 工具示例 ===\n")

    # 示例1: 基本用法 - 获取单个仓库信息
    print("1. 获取单个仓库信息:")
    try:
        repo_info = get_repo_info("openai", "openai-python")
        print(f"  仓库: {repo_info['full_name']}")
        print(f"  Star数: {repo_info['stars']}")
        print(f"  Fork数: {repo_info['forks']}")
        print(f"  描述: {repo_info['description']}")
        print(f"  主要语言: {repo_info['language']}")
        print(f"  创建时间: {repo_info['created_at'][:10]}")
        print(
            f"  标签: {', '.join(repo_info['topics'][:5]) if repo_info['topics'] else '无'}"
        )
    except Exception as e:
        print(f"  错误: {e}")

    print("\n" + "-" * 50 + "\n")

    # 示例2: 从URL获取
    print("2. 从GitHub URL获取仓库信息:")
    try:
        url_info = get_repo_info_from_url("https://github.com/langchain-ai/langchain")
        print(f"  仓库: {url_info['full_name']}")
        print(f"  Star数: {url_info['stars']}")
        print(f"  描述: {url_info['description']}")
    except Exception as e:
        print(f"  错误: {e}")

    print("\n" + "-" * 50 + "\n")

    # 示例3: 批量获取多个仓库
    print("3. 批量获取多个热门AI项目:")
    ai_projects = [
        "facebook/react",
        "tensorflow/tensorflow",
        {"owner": "microsoft", "repo": "vscode"},
        "https://github.com/pytorch/pytorch",
        "langchain-ai/langchain",
        "openai/openai-python",
    ]

    try:
        results = get_multiple_repos_info(ai_projects)
        for result in results:
            if "error" in result:
                print(f"  ❌ 错误: {result['input']} - {result['error']}")
            else:
                print(f"  ✅ {result['full_name']}: {result['stars']} stars")
    except Exception as e:
        print(f"  错误: {e}")

    print("\n" + "-" * 50 + "\n")

    # 示例4: 检查API限制
    print("4. 检查GitHub API限制:")
    try:
        rate_info = check_rate_limit()
        print(f"  剩余调用次数: {rate_info['remaining']}/{rate_info['limit']}")
        print(f"  已使用次数: {rate_info['used']}")
        print(f"  是否认证: {'是' if rate_info['is_authenticated'] else '否'}")
    except Exception as e:
        print(f"  错误: {e}")

    print("\n" + "-" * 50 + "\n")

    # 示例5: 使用GitHub Token（如果有的话）
    print("5. 使用GitHub Token（需要配置环境变量）:")
    import os
    from dotenv import load_dotenv

    # 加载环境变量
    load_dotenv()
    github_token = os.getenv("GITHUB_TOKEN")

    if github_token:
        print("  GitHub Token已配置，进行认证调用测试...")
        try:
            # 认证调用可以获得更高的API限制
            auth_rate_info = check_rate_limit(github_token)
            print(
                f"  认证后限制: {auth_rate_info['remaining']}/{auth_rate_info['limit']}"
            )
        except Exception as e:
            print(f"  错误: {e}")
    else:
        print("  未找到GITHUB_TOKEN环境变量，请在.env文件中配置")
        print("  或者设置环境变量: export GITHUB_TOKEN='your_token_here'")


if __name__ == "__main__":
    main()
