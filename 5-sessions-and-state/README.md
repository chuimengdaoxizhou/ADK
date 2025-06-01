# ADK 中的会话与状态管理

本示例演示如何在 ADK（Agent Development Kit）中创建并管理**有状态的会话（session）**，从而使你的代理（agent）能够在多轮交互中保持上下文，并记住用户信息。

---

## 什么是 ADK 中的会话？

ADK 中的会话功能可以实现以下目的：

1. **维护状态**：在多次交互中存储并访问用户数据、偏好等信息
2. **追踪对话历史**：自动记录并提取消息历史
3. **个性化响应**：利用存储的信息生成更有上下文、更个性化的回复

与那些每轮交互都“遗忘”的简单对话系统不同，有状态的 Agent 能够在多轮对话中建立对用户的理解，从而提供更贴近用户的体验。

---

## 示例概览

本目录下的示例演示了：

* 如何创建包含用户偏好的会话
* 如何在 agent 的指令中通过模板变量访问会话状态
* 如何结合 session 与 agent 运行，并在多轮对话中保持上下文

该示例构建了一个简单的问答 Agent，它会根据存储在 session 中的用户信息来作答。

---

## 项目结构

```
5-sessions-and-state/
│
├── basic_stateful_session.py      # 主示例脚本
│
└── question_answering_agent/      # Agent 实现目录
    ├── __init__.py
    └── agent.py                   # 包含模板变量的 Agent 定义
```

---

## 快速开始

### 环境配置

1. 激活项目根目录下的虚拟环境：

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 创建 `.env` 文件并填入你的 Google API 密钥：

```
GOOGLE_API_KEY=your_api_key_here
```

---

### 运行示例

运行以下命令体验一次有状态的会话：

```bash
python basic_stateful_session.py
```

该脚本将：

1. 创建一个包含用户信息的新会话
2. 使用该会话初始化 Agent
3. 处理一条与用户偏好相关的提问
4. 基于 session 中的信息返回个性化的响应

---

## 关键组件解释

### Session 服务

示例中使用 `InMemorySessionService`（内存中会话服务）来存储 session：

```python
session_service = InMemorySessionService()
```

---

### 初始状态

创建 session 时预设了包含用户信息的初始状态：

```python
initial_state = {
    "user_name": "Brandon Hancock",
    "user_preferences": """
        我喜欢打匹克球、飞盘高尔夫和网球。
        我最喜欢的食物是墨西哥菜。
        我最喜欢的电视剧是《权力的游戏》。
        我很高兴别人点赞和订阅我的 YouTube 频道。
    """,
}
```

---

### 创建 Session

你可以为某个用户创建一个带有唯一 ID 的 session：

```python
stateful_session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
```

---

### 在 Agent 指令中访问状态

Agent 可以通过模板变量访问 session 中的值：

```python
instruction="""
你是一个根据用户偏好回答问题的助手。

以下是关于用户的信息：
姓名：
{user_name}
偏好：
{user_preferences}
"""
```

---

### 与 Session 结合运行

使用 `Runner` 将 session 与 agent 结合，以维持多轮对话的状态：

```python
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service,
)
```

---

## 拓展资源

* [Google ADK 会话文档（官方）](https://google.github.io/adk-docs/sessions/session/)
* [ADK 中的状态管理文档](https://google.github.io/adk-docs/sessions/state/)

---

