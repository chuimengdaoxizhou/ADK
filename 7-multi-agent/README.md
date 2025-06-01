# ADK 中的多智能体系统（Multi-Agent Systems）

本示例展示了如何在 ADK 中创建多智能体系统，让多个专职智能体协同处理复杂任务，每个智能体各司其职。

## 什么是多智能体系统？

多智能体系统是一种 ADK 中的高级模式，它允许多个专门的智能体协作处理复杂任务。每个智能体可以专注于某一特定领域或功能，并通过委托和通信协作，解决单个智能体难以应对的问题。

## 项目结构要求

为了让多智能体系统在 ADK 中正常工作，项目必须遵循特定结构：

```
parent_folder/
├── root_agent_folder/           # 主智能体包（如 "manager"）
│   ├── __init__.py              # 必须导入 agent.py
│   ├── agent.py                 # 必须定义 root_agent
│   ├── .env                     # 环境变量
│   └── sub_agents/              # 所有子智能体的目录
│       ├── __init__.py          # 可为空，或导入子智能体
│       ├── agent_1_folder/      # 子智能体包
│       │   ├── __init__.py      # 必须导入 agent.py
│       │   └── agent.py         # 必须定义一个 agent 变量
│       ├── agent_2_folder/
│       │   ├── __init__.py
│       │   └── agent.py
│       └── ...
```

### 关键结构组成：

1. **主智能体包（Root Agent Package）**

   * 必须遵循标准智能体结构（如基础 agent 示例）
   * `agent.py` 中必须定义一个 `root_agent` 变量

2. **子智能体目录（Sub-agents Directory）**

   * 通常放在主智能体包下的 `sub_agents` 目录中
   * 每个子智能体在一个单独文件夹中，遵循普通智能体结构

3. **导入子智能体**

   * 主智能体必须导入子智能体才能使用：

     ```python
     from .sub_agents.funny_nerd.agent import funny_nerd
     from .sub_agents.stock_analyst.agent import stock_analyst
     ```

4. **命令执行位置**

   * 始终从父目录（如 `6-multi-agent`）运行 `adk web`，不要从 agent 子目录中运行

以上结构可确保 ADK 能正确发现和加载所有层级的智能体。

## 多智能体架构模式

ADK 支持两种主要的多智能体架构方式：

### 1. 子智能体委托模式（Sub-Agent Delegation Model）

使用 `sub_agents` 参数，主智能体可将任务完全委托给专职智能体：

```python
root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="管理者智能体",
    instruction="你是一个管理者，将任务委托给专门的智能体...",
    sub_agents=[stock_analyst, funny_nerd],
)
```

**特点：**

* 完全委托：子智能体接管整个回复
* 子智能体决定最终响应内容
* 主智能体充当“路由器”角色，决定由谁处理用户请求

### 2. 智能体作为工具（Agent-as-a-Tool）模式

使用 `AgentTool` 封装器，将其他智能体作为工具供主智能体调用：

```python
from google.adk.tools.agent_tool import AgentTool

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="管理者智能体",
    instruction="你是一个使用专职智能体作为工具的管理者...",
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)
```

**特点：**

* 子智能体将结果返回主智能体
* 主智能体保持控制权，可整合多个子智能体的响应
* 可以在一个回复中调用多个“智能体工具”
* 灵活性更高

## 多智能体限制说明

### 子智能体中的限制

**子智能体中不能使用内置工具。**

例如，以下方式目前**不被支持**：

```python
search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="你是谷歌搜索专家",
    tools=[google_search],  # 内置工具
)
coding_agent = Agent(
    model='gemini-2.0-flash',
    name='CodeAgent',
    instruction="你是代码执行专家",
    tools=[built_in_code_execution],  # 内置工具
)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="Root Agent",
    sub_agents=[
        search_agent,  # 不支持
        coding_agent   # 不支持
    ],
)
```

### 使用 AgentTool 的解决方案

要同时使用多个内置工具，或结合使用自定义工具与内置工具，推荐使用 `AgentTool` 方式：

```python
from google.adk.tools import agent_tool

search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="你是谷歌搜索专家",
    tools=[google_search],
)
coding_agent = Agent(
    model='gemini-2.0-flash',
    name='CodeAgent',
    instruction="你是代码执行专家",
    tools=[built_in_code_execution],
)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="Root Agent",
    tools=[
        agent_tool.AgentTool(agent=search_agent), 
        agent_tool.AgentTool(agent=coding_agent)
    ],
)
```

该方式将智能体封装为工具，允许主智能体灵活调用并整合结果。

## 示例：我们的多智能体系统

本示例构建了一个“管理者”智能体，协作调用三个专职智能体：

1. **Stock Analyst（股市分析师）**（子智能体）：提供金融信息和股市分析
2. **Funny Nerd（搞笑极客）**（子智能体）：生成有关技术话题的搞笑内容
3. **News Analyst（新闻分析师）**（作为 AgentTool 工具）：摘要当前科技新闻

管理者会根据用户输入内容，路由到合适的智能体处理。

## 快速开始

本示例使用的是主目录中创建的虚拟环境，请确保：

1. 激活虚拟环境：

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 设置 API 密钥：

   * 将 `manager` 文件夹下的 `.env.example` 重命名为 `.env`
   * 在 `.env` 中添加你的 Google API Key，例如：

     ```
     GOOGLE_API_KEY=你的密钥
     ```

## 运行示例

1. 进入包含 agent 文件夹的 `6-multi-agent` 目录：

```bash
cd 6-multi-agent
```

2. 启动 Web UI：

```bash
adk web
```

3. 打开终端显示的地址（通常是 [http://localhost:8000）](http://localhost:8000）)

4. 在左上角下拉框中选择 "manager" 智能体

5. 在底部输入框中与智能体对话

### 常见问题排查

如果下拉列表中未正确显示你的多智能体设置，请确认：

* 你是否从父目录（如 `6-multi-agent`）运行了 `adk web`
* 每个 agent 的 `__init__.py` 是否正确导入了 `agent.py`
* 根智能体是否正确导入了所有子智能体

### 示例提示语

你可以尝试以下输入：

* “今天的股市怎么样？”
* “说一个关于编程的搞笑段子”
* “最近的科技新闻有哪些？”
* “现在几点了？”

按下 `Ctrl+C` 可退出会话或关闭服务器。

## 更多资源

* [ADK 多智能体系统官方文档](https://google.github.io/adk-docs/agents/multi-agent-systems/)
* [AgentTool 使用文档](https://google.github.io/adk-docs/tools/function-tools/#3-agent-as-a-tool)

---

