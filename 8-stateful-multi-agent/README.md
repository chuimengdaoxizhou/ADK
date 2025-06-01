# ADK中的有状态多智能体系统

本示例展示了如何在ADK中创建一个有状态的多智能体系统，将持久化状态管理与专门化智能体委派相结合。这种方法创建了智能的代理系统，能够在多次交互中记住用户信息，并利用专门化领域的知识。

## 什么是有状态多智能体系统？

有状态多智能体系统结合了两种强大的模式：

1. **状态管理**：在多次交互中持久化用户信息和对话历史
2. **多智能体架构**：根据专门化的知识将任务分配给不同的智能体

最终结果是一个复杂的智能体生态系统，能够：

* 记住用户信息和交互历史
* 将查询路由到最合适的专门化智能体
* 根据过去的互动提供个性化的回应
* 在多个智能体代理之间维持上下文

本示例实现了一个在线课程平台的客户服务系统，其中专门的智能体处理不同方面的客户支持，同时共享一个共同的状态。

## 项目结构

```
7-stateful-multi-agent/
│
├── customer_service_agent/         # 主智能体包
│   ├── __init__.py                 # ADK发现所需
│   ├── agent.py                    # 根智能体定义
│   └── sub_agents/                 # 专门化的智能体
│       ├── course_support_agent/   # 处理课程内容问题
│       ├── order_agent/            # 管理订单历史和退款
│       ├── policy_agent/           # 解答政策问题
│       └── sales_agent/            # 处理课程购买
│
├── main.py                         # 应用入口，包含会话设置
├── utils.py                        # 状态管理的辅助函数
├── .env                            # 环境变量
└── README.md                       # 本文档
```

## 关键组件

### 1. 会话管理

本示例使用`InMemorySessionService`来存储会话状态：

```python
session_service = InMemorySessionService()

def initialize_state():
    """初始化会话状态，设置默认值。"""
    return {
        "user_name": "Brandon Hancock",
        "purchased_courses": [""],
        "interaction_history": [],
    }

# 创建一个带有初始状态的新会话
session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initialize_state(),
)
```

### 2. 状态共享

系统中的所有智能体都可以访问相同的会话状态，从而实现：

* 根智能体跟踪交互历史
* 销售智能体更新已购买课程
* 课程支持智能体检查用户是否已购买特定课程
* 所有智能体根据用户信息提供个性化响应

### 3. 多智能体委派

客户服务智能体将查询路由到专门的子智能体：

```python
customer_service_agent = Agent(
    name="customer_service",
    model="gemini-2.0-flash",
    description="AI开发者加速器社区的客户服务智能体",
    instruction="""
    你是AI开发者加速器社区的主要客户服务智能体。
    你的角色是帮助用户解决问题，并将他们引导到适当的专门智能体。
    
    # ... 详细的指令 ...
    
    """,
    sub_agents=[policy_agent, sales_agent, course_support_agent, order_agent],
    tools=[get_current_time],
)
```

## 工作原理

1. **初始化会话**：

   * 创建一个新的会话，包含用户信息和空的交互历史
   * 会话状态使用默认值进行初始化

2. **对话追踪**：

   * 每个用户消息都会添加到`interaction_history`（交互历史）中
   * 智能体可以查看过去的交互，保持上下文

3. **查询路由**：

   * 根智能体分析用户查询，决定应该由哪个专家来处理
   * 专门化的智能体在被委派时会接收到完整的状态上下文

4. **状态更新**：

   * 当用户购买课程时，销售智能体会更新`purchased_courses`（已购买课程）
   * 所有智能体都可以使用这些更新的信息进行后续交互

5. **个性化响应**：

   * 智能体根据购买历史和过去的互动来调整响应
   * 根据用户已购买的课程不同，系统会采取不同的路径

## 快速开始

### 设置

1. 激活根目录中的虚拟环境：

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 确保在`.env`文件中设置了您的Google API密钥：

```
GOOGLE_API_KEY=your_api_key_here
```

### 运行示例

运行有状态的多智能体示例：

```bash
python main.py
```

这将：

1. 初始化一个带有默认状态的新会话
2. 启动与客户服务智能体的交互式对话
3. 跟踪所有交互历史
4. 允许专门智能体处理特定的查询

### 示例对话流程

尝试以下对话流程以测试系统：

1. **从一般查询开始**：

   * "你们提供哪些课程？"
   * （根智能体将查询路由到销售智能体）

2. **询问购买信息**：

   * "我想购买AI营销平台课程"
   * （销售智能体将处理购买并更新状态）

3. **询问课程内容**：

   * "你能告诉我AI营销平台课程的内容吗？"
   * （根智能体将查询路由到课程支持智能体，后者已能访问相关信息）

4. **询问退款政策**：

   * "你们的退款政策是什么？"
   * （根智能体将查询路由到政策智能体）

注意，系统会跨不同的专门智能体记住您的购买信息！

## 高级功能

### 1. 交互历史跟踪

系统维护交互历史，以提供上下文：

```python
# 更新交互历史，添加用户的查询
add_user_query_to_history(
    session_service, APP_NAME, USER_ID, SESSION_ID, user_input
)
```

### 2. 动态访问控制

系统实现了条件访问某些智能体的功能：

```
3. 课程支持智能体
   - 处理关于课程内容的问题
   - 仅当用户购买了该课程后才可访问
   - 在将用户引导到此智能体之前，检查"ai_marketing_platform"是否在已购买课程列表中
```

### 3. 基于状态的个性化

所有智能体根据会话状态调整响应：

```
根据用户的购买历史和过去的交互调整你的回应。
当用户还没有购买任何课程时，鼓励他们探索AI营销平台。
当用户已购买课程时，提供与这些课程相关的支持。
```

## 生产考虑事项

对于生产实现，考虑：

1. **持久化存储**：将`InMemorySessionService`替换为`DatabaseSessionService`，以便在应用重启时保持会话状态
2. **用户认证**：实施适当的用户认证机制，确保安全地识别用户
3. **错误处理**：为智能体故障和状态损坏添加健壮的错误处理机制
4. **监控**：实现日志记录和监控系统，以跟踪系统性能

## 其他资源

* [ADK会话文档](https://google.github.io/adk-docs/sessions/session/)
* [ADK多智能体系统文档](https://google.github.io/adk-docs/agents/multi-agent-systems/)
* [ADK中的状态管理](https://google.github.io/adk-docs/sessions/state/)
