# ADK 中的持久化存储

本示例演示了如何为你的 ADK 智能体实现持久化存储，使其能够记住信息，并在多次会话、应用程序重启甚至服务器重新部署后仍能保持对话历史。

---

## 什么是 ADK 中的持久化存储？

在之前的示例中，我们使用了 `InMemorySessionService`，它只将会话数据保存在内存中——一旦应用程序停止运行，数据就会丢失。而在真实的应用场景中，通常需要智能体长期记住用户信息和对话历史。这时就需要 **持久化存储**。

ADK 提供了 `DatabaseSessionService`，可以将会话数据保存在 SQL 数据库中，从而实现：

1. **长期记忆**：数据在程序重启后仍然存在
2. **一致的用户体验**：用户可以从上次中断的地方继续对话
3. **多用户支持**：不同用户的数据是隔离并安全的
4. **可扩展性**：支持用于大规模生产环境的数据库系统

本示例通过使用 SQLite 数据库，展示了如何实现一个能记住用户姓名和待办事项的提醒助手（reminder agent）。

---

## 项目结构

```
5-persistent-storage/
│
├── memory_agent/               # 智能体包
│   ├── __init__.py             # 用于 ADK 发现 agent 的标志文件
│   └── agent.py                # 定义包含提醒工具的智能体
│
├── main.py                     # 应用主入口，负责设置数据库会话服务
├── utils.py                    # 辅助工具函数，支持终端 UI 和智能体交互
├── .env                        # 环境变量文件
├── my_agent_data.db            # SQLite 数据库文件（首次运行时创建）
└── README.md                   # 本文档
```

---

## 核心组件

### 1. `DatabaseSessionService`

实现持久化的核心是 `DatabaseSessionService`，它通过数据库 URL 初始化：

```python
from google.adk.sessions import DatabaseSessionService

db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)
```

该服务可以：

* 将会话数据存入 SQLite 数据库文件
* 为用户检索先前的会话
* 自动管理数据库表结构和 schema

---

### 2. 会话管理

示例中展示了如何管理会话：

```python
# 检查当前用户是否已有会话
existing_sessions = session_service.list_sessions(
    app_name=APP_NAME,
    user_id=USER_ID,
)

# 如果已有会话，则继续使用；否则创建新的会话
if existing_sessions and len(existing_sessions.sessions) > 0:
    SESSION_ID = existing_sessions.sessions[0].id
    print(f"继续使用已有会话: {SESSION_ID}")
else:
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initialize_state(),
    )
```

---

### 3. 使用工具管理状态（state）

智能体中定义的工具会自动更新持久化状态：

```python
def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    # 获取当前提醒列表
    reminders = tool_context.state.get("reminders", [])
    
    # 添加新提醒
    reminders.append(reminder)
    
    # 更新状态
    tool_context.state["reminders"] = reminders
    
    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"已添加提醒: {reminder}",
    }
```

所有对 `tool_context.state` 的修改会自动保存到数据库中。

---

## 快速开始

### 先决条件

* Python 3.9+
* 用于 Gemini 模型的 Google API Key
* SQLite（Python 已内置）

---

### 项目设置

1. 激活虚拟环境：

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 在 `.env` 文件中设置你的 Google API 密钥：

```
GOOGLE_API_KEY=your_api_key_here
```

---

### 运行示例

使用以下命令运行持久化存储示例：

```bash
python main.py
```

此命令将执行以下操作：

1. 连接或创建 SQLite 数据库
2. 检查当前用户是否已有会话
3. 启动智能体对话
4. 将所有对话记录保存至数据库

---

## 示例交互

你可以尝试以下对话来测试记忆功能：

### 第一次运行：

* “我的名字是什么？”
* “我叫 John”
* “添加一个提醒：买菜”
* “再添加一个提醒：完成报告”
* “我有哪些提醒？”
* 输入 "exit" 退出程序

### 第二次运行：

* “我的名字是什么？”
* “我有哪些提醒？”
* “把第二个提醒更新为：周五前提交报告”
* “删除第一个提醒”

无论退出程序还是重启系统，智能体都能记住之前的对话内容。

---

## 在生产环境中使用数据库存储

虽然本示例使用 SQLite 来简化操作，`DatabaseSessionService` 实际上支持通过 SQLAlchemy 使用各种数据库后端，例如：

* PostgreSQL：`postgresql://user:password@localhost/dbname`
* MySQL：`mysql://user:password@localhost/dbname`
* MS SQL Server：`mssql://user:password@localhost/dbname`

### 在生产中使用的建议：

1. 选择适合你规模需求的数据库系统
2. 配置数据库连接池提高性能
3. 加强数据库凭据的安全性
4. 为关键数据做好备份策略

---

## 其他资源

* 📄 [ADK 会话文档](https://google.github.io/adk-docs/sessions/session/)
* 🧩 [SessionService 实现](https://google.github.io/adk-docs/sessions/session/#sessionservice-implementations)
* 🔧 [ADK 状态管理](https://google.github.io/adk-docs/sessions/state/)
* 📘 [SQLAlchemy 文档](https://docs.sqlalchemy.org/)（高级数据库配置）

---


