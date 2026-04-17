# GitHub API 工具

这个工具提供了从GitHub API获取仓库基本信息的Python函数。

## 功能

- 获取GitHub仓库的基本信息（Star数、Fork数、描述等）
- 格式化输出仓库信息
- 将仓库信息保存为JSON文件
- 支持使用GitHub Token提高API速率限制

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基础用法

```python
from utils.github_api import get_repo_info, format_repo_info, save_repo_info_to_file

# 获取仓库信息
repo_info = get_repo_info("anomalyco", "opencode")

# 格式化输出
print(format_repo_info(repo_info))

# 保存到文件
save_repo_info_to_file(repo_info, "repo_info.json")
```

### 使用GitHub Token

```python
# 使用GitHub Token（可选，用于提高速率限制）
repo_info = get_repo_info("anomalyco", "opencode", token="your_github_token_here")
```

### 直接运行示例

```bash
python utils/github_api.py
```

## 返回的信息

函数返回一个包含以下信息的字典：
- `name`: 仓库名称
- `full_name`: 仓库完整名称
- `description`: 仓库描述
- `stars`: Star数
- `forks`: Fork数
- `watchers`: Watch数
- `open_issues`: 未关闭的issue数
- `language`: 主要编程语言
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `html_url`: GitHub页面URL
- 以及其他相关信息

## 注意事项

1. 未认证的GitHub API请求每小时限制为60次
2. 使用GitHub Token可将限制提高到5000次/小时
3. 函数包含错误处理，会返回包含错误信息的字典

## 示例输出

```
仓库: anomalyco/opencode
描述: 无描述
⭐ Stars: 0
🍴 Forks: 0
👁️ Watchers: 0
🐛 未关闭Issues: 0
主要语言: 未知
许可证: 无
默认分支: main
创建时间: 未知
最后更新: 未知
GitHub页面: https://github.com/anomalyco/opencode
```