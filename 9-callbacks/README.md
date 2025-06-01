# 🔁 ADK 中的回调机制详解（Callbacks）

在 Agent Developer Kit（ADK）中，**回调机制**允许开发者在代理执行流程中的关键节点插入自定义逻辑，例如拦截请求、修改模型响应、跟踪工具调用等。你可以用它来实现日志记录、安全控制、动态参数注入或内容重写等功能。

---

## 🧠 什么是回调？

回调是指在系统执行某个操作前后，调用你自定义的函数，从而让你“插手”代理执行过程。例如：

* 在代理运行前记录日志（如请求时间）
* 拦截模型请求并过滤敏感词
* 修改工具返回的结果内容

---

## 📦 回调的三种类型

| 回调类型 | 调用时机      | 作用示例             |
| ---- | --------- | ---------------- |
| 代理回调 | 代理运行前后    | 日志、状态记录、权限控制等    |
| 模型回调 | 模型请求前/响应后 | 内容过滤、响应替换、日志记录等  |
| 工具回调 | 工具调用前/调用后 | 参数预处理、结果增强、审计记录等 |

---

## 🛠 回调上下文对象

所有回调函数都可访问 **上下文对象**（如 `CallbackContext`, `LlmRequest`, `ToolContext`），用于访问状态、请求参数等：

### 🧩 `CallbackContext`

用于访问全局上下文，包括状态和元信息：

```python
callback_context.agent_name     # 当前代理名称
callback_context.user_id        # 用户 ID
callback_context.state["x"]     # 状态存取（可跨请求）
callback_context.invocation_id  # 当前调用唯一 ID
```

### 📨 `LlmRequest`

用于 `before_model_callback`，可读取请求文本内容：

```python
llm_request.contents      # 消息内容（对话历史）
llm_request.generation_config  # 模型生成配置
```

### 📤 `LlmResponse`

用于 `after_model_callback`，可修改模型返回的内容：

```python
llm_response.content.parts[0].text  # 模型回复文本
```

### 🧰 `ToolContext`

用于工具回调，可访问工具输入输出和状态：

```python
tool_context.state["last_tool"] = tool.name
```

---

## 🧪 示例一：代理回调（before / after）

路径：`before_after_agent/agent.py`

### 👇 before\_agent\_callback

```python
def before_agent_callback(callback_context: CallbackContext):
    state = callback_context.state
    state["request_counter"] = state.get("request_counter", 0) + 1
    state["start_time"] = datetime.now()
    logger.info(f"Agent {callback_context.agent_name} 开始执行")
```

### ☝ after\_agent\_callback

```python
def after_agent_callback(callback_context: CallbackContext):
    state = callback_context.state
    duration = datetime.now() - state.get("start_time", datetime.now())
    logger.info(f"执行耗时：{duration.total_seconds()} 秒")
```

---

## 🤖 示例二：模型回调（before / after）

路径：`before_after_model/agent.py`

### ❗before\_model\_callback：屏蔽不当内容

```python
def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest):
    user_msg = next(
        (p.text for c in reversed(llm_request.contents) if c.role == "user" for p in c.parts),
        None
    )
    if user_msg and "sucks" in user_msg:
        return LlmResponse(
            content=types.Content(role="model", parts=[
                types.Part(text="我无法处理带有不当词语的请求。")
            ])
        )
```

### ✏ after\_model\_callback：替换负面词语

```python
def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse):
    if llm_response.content and llm_response.content.parts:
        text = llm_response.content.parts[0].text
        text = text.replace("problem", "challenge").replace("difficult", "complex")
        llm_response.content.parts[0].text = text
        return llm_response
```

---

## 🧰 示例三：工具回调（before / after）

路径：`before_after_tool/agent.py`

### ✨ before\_tool\_callback：动态参数替换

```python
def before_tool_callback(tool, tool_input, tool_context: ToolContext):
    if tool_input.get("location") == "here":
        tool_input["location"] = "San Francisco"
        return tool_input
```

### 📎 after\_tool\_callback：结果增强

```python
def after_tool_callback(tool, tool_input, tool_output, tool_context: ToolContext):
    if isinstance(tool_output, str):
        return f"{tool_output}\n\n（来源：示例工具）"
```

---

## 📁 示例项目结构

```
8-callbacks/
├── before_after_agent/       # 代理回调示例
├── before_after_model/       # 模型回调示例
├── before_after_tool/        # 工具回调示例
└── README.md                 # 文档（即本文件）
```

---

## 🧪 示例测试建议

* 输入："This website sucks, can you help me?" → 触发模型回调拦截
* 输入："I'm facing a difficult problem." → 触发模型响应替换
* 输入："What's the weather like **here**?" → 工具参数自动改为 San Francisco

---

## 🧠 总结：回调机制适合做什么？

| 用途      | 示例                 |
| ------- | ------------------ |
| 🔍 日志审计 | 打印代理运行日志、模型响应统计    |
| 🧼 安全控制 | 过滤敏感词、拦截风险请求       |
| 🧩 数据改写 | 修改模型回复、工具参数、增强响应内容 |
| 📦 状态注入 | 在代理会话状态中共享数据       |

---

