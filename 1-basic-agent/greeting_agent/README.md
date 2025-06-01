# 基础 ADK Agent 示例

## 什么是 ADK Agent？

`LlmAgent`（通常简称为 `Agent`）是 ADK 中的核心组件，负责你应用中的“思考”部分。它利用大型语言模型（LLM）的能力来实现：

* 推理
* 理解自然语言
* 做决策
* 生成回复
* 与工具交互

不同于遵循预设路径的确定性工作流代理，`LlmAgent` 的行为是非确定性的。它使用 LLM 来解读指令和上下文，动态决定下一步如何行动，是否使用工具，或者是否将控制权转交给其他代理。

## 必须的代理结构

为了让 ADK 能正确发现并运行你的代理（尤其是在运行 `adk web` 时），你的项目必须遵循特定的目录结构：

```
parent_folder/
    agent_folder/         # 这是你的代理包目录
        __init__.py       # 必须导入 agent.py
        agent.py          # 必须定义 root_agent
        .env              # 环境变量文件
```

### 关键组成：

1. **`__init__.py`**

   * 必须导入代理模块：`from . import agent`
   * 这样 ADK 才能发现你的代理

2. **`agent.py`**

   * 必须定义一个名为 `root_agent` 的变量
   * ADK 会以此作为代理的入口点

3. **命令执行位置**

   * 运行 `adk` 命令时一定要在父目录下，而不是进入代理目录中执行
   * 例如，在包含代理文件夹的父目录中运行 `adk web`

这个结构确保 ADK 在运行 `adk web` 或 `adk run` 等命令时，能够自动发现并加载你的代理。

## 主要组件

### 1. 身份信息（`name` 和 `description`）

* **name**（必填）：代理的唯一字符串标识
* **description**（可选但推荐）：对代理能力的简洁描述，方便其他代理判断是否要把任务转给它

### 2. 模型（`model`）

* 指定为该代理提供能力的 LLM，例如 `"gemini-2.0-flash"`
* 影响代理能力、成本和性能

### 3. 指令（`instruction`）

这是塑造代理行为的最关键参数，定义了：

* 核心任务或目标
* 性格或角色定位
* 行为约束
* 工具的使用方法
* 输出格式要求

### 4. 工具（`tools`）

可选，为代理提供除 LLM 内建知识外的能力，让代理能够：

* 与外部系统交互
* 执行计算
* 获取实时数据
* 执行特定操作

## 快速开始

本示例使用在根目录创建的虚拟环境，确保你已经：

1. 从根目录激活虚拟环境：

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 设置你的 API Key：

* 将 `greeting_agent` 文件夹中的 `.env.example` 重命名为 `.env`
* 在 `.env` 文件中添加你的 Google API Key 到 `GOOGLE_API_KEY` 变量

## 运行示例

运行该基础代理示例时，使用 ADK CLI 工具，支持多种交互方式：

1. 进入包含你的代理文件夹的 `1-basic-agent` 目录
2. 启动交互式网页界面：

```bash
adk web
```

3. 在终端显示的地址打开网页（一般是 [http://localhost:8000）](http://localhost:8000）)

4. 在网页左上角的下拉菜单中选择你的代理

5. 在页面底部的输入框开始与代理聊天

### 常见问题排查

如果代理没有出现在下拉菜单中：

* 确认你是在父目录（如 `1-basic-agent`）运行 `adk web`，而不是进入代理目录后运行
* 确认 `__init__.py` 文件中正确导入了代理模块
* 确认 `agent.py` 中定义了 `root_agent`

### 其他运行方式

ADK CLI 还提供其他运行选项：

* **`adk web`**：启动带聊天界面的网页 UI
* **`adk run [agent_name]`**：在终端直接运行指定代理
* **`adk api_server`**：启动 FastAPI 服务器，用于测试 API 请求

按 `Ctrl+C` 可退出对话或停止服务器。

本示例展示了一个简单的问候代理，演示了如何使用 ADK 创建代理的基本流程。
