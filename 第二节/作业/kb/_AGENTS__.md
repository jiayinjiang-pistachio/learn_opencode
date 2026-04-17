# AI 知识库助手项目 - Agents 规范

## 1. 项目概述

一个自动化的 AI 知识库助手，通过多智能体协作从 GitHub Trending 和 Hacker News 采集 AI/LLM/Agent 领域技术动态，经 AI 分析结构化后存储为 JSON，并支持 Telegram/飞书等多渠道分发。

## 2. 技术栈

- **运行时**: Python 3.12+
- **AI 框架**: OpenCode + 国产大模型 (DeepSeek/GLM/Baichuan)
- **Agent 编排**: Langraph
- **数据采集**: OpenClaw (GitHub Trending, Hacker News API)
- **数据存储**: JSON 文件 (暂定，后续可迁移到数据库)
- **消息分发**: Telethon (Telegram), Feishu OpenAPI

## 3. 编码规范

- **代码风格**: PEP 8 标准
- **命名约定**: snake_case (变量、函数、文件)
- **文档注释**: Google 风格 docstring
- **日志规范**: 使用 logging 模块，禁止裸 `print()`
- **类型提示**: 尽可能使用 Type Hints
- **异常处理**: 明确的异常捕获和日志记录
- **配置文件**: 使用 `.env` 文件管理敏感信息

## 4. 项目结构

```
kb/
├── README.md
├── AGENTS.md
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── collector/
│   │   │   ├── __init__.py
│   │   │   ├── github_trending.py
│   │   │   ├── hacker_news.py
│   │   │   └── base_collector.py
│   │   ├── analyzer/
│   │   │   ├── __init__.py
│   │   │   ├── content_analyzer.py
│   │   │   └── relevance_filter.py
│   │   └── organizer/
│   │       ├── __init__.py
│   │       ├── data_formatter.py
│   │       └── deduplicator.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── json_store.py
│   │   └── knowledge_entry.py
│   ├── distribution/
│   │   ├── __init__.py
│   │   ├── telegram_bot.py
│   │   ├── feishu_bot.py
│   │   └── message_formatter.py
│   └── orchestration/
│       ├── __init__.py
│       └── workflow.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── knowledge_base.json
├── logs/
├── tests/
└── scripts/
    └── run_pipeline.py
```

## 5. 知识条目 JSON 格式

```json
{
  "id": "uuid4_or_hash",
  "title": "文章标题或项目名称",
  "source_url": "原始链接",
  "source_type": "github_trending|hacker_news",
  "summary": "AI 生成的简要总结 (200-300 字)",
  "content": "原始内容或关键信息",
  "tags": ["llm", "agent", "framework", "research"],
  "category": "framework|tool|paper|blog|news",
  "relevance_score": 0.95,
  "status": "pending|processed|archived",
  "created_at": "2024-01-01T00:00:00Z",
  "processed_at": "2024-01-01T00:00:00Z",
  "metadata": {
    "stars": 1234,
    "language": "Python",
    "author": "作者/组织",
    "publish_date": "2024-01-01",
    "read_time_minutes": 5
  }
}
```

## 6. Agent 角色概览

| 角色 | 职责 | 技术实现 | 输出 |
|------|------|----------|------|
| **采集器** | 从 GitHub Trending 和 Hacker News 获取原始数据 | OpenClaw + 定时任务 | 原始数据列表 |
| **分析器** | AI 分析内容相关性、生成摘要、打标签 | OpenCode + 大模型 | 结构化分析结果 |
| **整理器** | 格式化、去重、存储到知识库 | 数据处理逻辑 | 标准化的知识条目 |

### 6.1 采集器 (Collector Agent)
- **GitHubTrendingCollector**: 获取 GitHub Trending 中的 AI/LLM 相关项目
- **HackerNewsCollector**: 爬取 Hacker News 上与 AI 相关的热门帖子
- **数据过滤**: 基于关键词初步过滤 (LLM, Agent, AI, GPT, Claude, 等)

### 6.2 分析器 (Analyzer Agent)
- **内容分析**: 使用大模型理解内容，判断与 AI 领域的相关性
- **摘要生成**: 生成 200-300 字的简要总结
- **标签分类**: 自动打上相关标签 (llm, agent, framework, tool, research 等)
- **质量评分**: 计算内容质量分数 (0-1)

### 6.3 整理器 (Organizer Agent)
- **数据格式化**: 转换为标准 JSON 格式
- **去重处理**: 基于 URL 和内容哈希去重
- **数据存储**: 保存到知识库文件
- **状态管理**: 更新条目状态 (pending → processed → archived)

## 7. 工作流设计

```
GitHub Trending → Collector → Analyzer → Organizer → Storage
Hacker News     ↗         ↗         ↗         ↗          ↓
                                               Telegram/飞书分发
```

## 8. 红线 (绝对禁止的操作)

1. **禁止硬编码敏感信息**: API Key、Token、密码等必须通过环境变量管理
2. **禁止裸 `print()`**: 所有日志必须通过 logging 模块记录
3. **禁止破坏性操作**: 不删除或修改原始采集数据，只追加新数据
4. **禁止绕过错误处理**: 所有可能失败的操作必须有异常捕获和日志
5. **禁止直接调用外部 API**: 必须通过配置的代理或合法渠道
6. **禁止存储 PII**: 不收集或存储个人身份信息
7. **禁止无限循环**: 所有循环必须有明确的退出条件和超时机制
8. **禁止同步阻塞操作**: 长时间操作必须异步或使用超时
9. **禁止未经验证的 AI 输出**: AI 生成的内容必须经过验证和清理
10. **禁止绕过代码审查**: 所有代码变更必须经过 review 流程

## 9. 部署与运行

### 9.1 环境配置
```bash
# 复制环境变量模板
cp .env.example .env
# 编辑 .env 文件配置 API Key 等

# 安装依赖
pip install -r requirements.txt
```

### 9.2 运行流程
```bash
# 运行完整流程
python scripts/run_pipeline.py

# 单独运行采集
python -m src.agents.collector.github_trending

# 查看日志
tail -f logs/kb_agent.log
```

### 9.3 定时任务 (Cron)
```
# 每天 9:00 和 18:00 运行
0 9,18 * * * cd /path/to/kb && python scripts/run_pipeline.py
```

## 10. 监控与维护

- **日志级别**: INFO (生产), DEBUG (开发)
- **健康检查**: `/health` 端点或定期心跳
- **数据备份**: 定期备份 knowledge_base.json
- **性能监控**: 记录每个步骤的执行时间
- **错误报警**: 关键错误通过消息渠道通知

---

*最后更新: 2024-04-17*
*版本: 1.0.0*
