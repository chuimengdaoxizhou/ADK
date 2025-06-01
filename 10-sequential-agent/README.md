# ADK 中的顺序代理（Sequential Agents）

本示例演示了如何在 Agent Development Kit (ADK) 中实现顺序代理。主代理 `lead_qualification_agent` 是一个顺序代理，按预定顺序依次执行子代理，每个代理的输出将作为下一个代理的输入。

## 什么是顺序代理？

顺序代理是 ADK 中的一种**工作流代理（workflow agents）**，其特点包括：

1. **按固定顺序执行**：子代理按指定顺序一个接一个地运行
2. **在代理之间传递数据**：通过状态管理机制，在代理之间传递信息
3. **创建处理流水线**：非常适合每一步都依赖前一步输出的场景

当你需要一个确定性的、逐步执行的工作流，且执行顺序很关键时，应使用顺序代理。

## 潜在客户资格审核流水线示例

在本示例中，我们创建了一个名为 `lead_qualification_agent` 的顺序代理，用于为销售团队实现潜在客户资格审核的流水线。该顺序代理组织协调以下三个子代理：

1. **线索验证代理（Lead Validator Agent）**：检查线索信息是否足够完善以进入资格审核

   * 验证是否包含必要信息，如联系方式和兴趣点
   * 输出“有效”或“无效”以及原因说明

2. **线索评分代理（Lead Scorer Agent）**：对有效线索进行 1-10 的评分

   * 分析因素包括：紧迫性、决策权、预算和时间表
   * 给出数值评分并附上简短的理由

3. **行动推荐代理（Action Recommender Agent）**：基于验证和评分结果推荐下一步行动

   * 对无效线索：建议收集哪些额外信息
   * 对低分线索（1-3 分）：建议进行培育（nurturing）
   * 对中等分线索（4-7 分）：建议进行资格确认（qualifying）
   * 对高分线索（8-10 分）：建议直接销售行动

### 工作流程说明

`lead_qualification_agent` 顺序代理的执行顺序如下：

1. 首先运行验证器，判断线索信息是否完整
2. 然后运行评分器（可以访问验证结果的状态）
3. 最后运行推荐器（可以访问验证和评分的结果）

每个子代理的输出通过 `output_key` 参数存储在会话状态中：

* `validation_status`
* `lead_score`
* `action_recommendation`

## 项目结构

```
9-sequential-agent/
│
├── lead_qualification_agent/       # 主顺序代理包
│   ├── __init__.py                 # 包初始化文件
│   ├── agent.py                    # 顺序代理定义（root_agent）
│   │
│   └── subagents/                  # 子代理文件夹
│       ├── __init__.py             # 子代理初始化
│       │
│       ├── validator/              # 线索验证代理
│       │   ├── __init__.py
│       │   └── agent.py
│       │
│       ├── scorer/                 # 线索评分代理
│       │   ├── __init__.py
│       │   └── agent.py
│       │
│       └── recommender/            # 行动推荐代理
│           ├── __init__.py
│           └── agent.py
│
├── .env.example                    # 环境变量示例文件
└── README.md                       # 本文档
```

## 快速开始

### 环境配置

1. 在项目根目录下激活虚拟环境：

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 复制 `.env.example` 为 `.env`，并填写你的 Google API Key：

```
GOOGLE_API_KEY=your_api_key_here
```

### 运行示例

```bash
cd 9-sequential-agent
adk web
```

然后在 Web UI 中选择 `lead_qualification_agent` 代理进行交互。

## 示例交互

你可以尝试如下输入示例：

### 合格线索示例：

```
线索信息：
姓名：Sarah Johnson
邮箱：sarah.j@techinnovate.com
电话：555-123-4567
公司：Tech Innovate Solutions
职位：CTO
兴趣：希望使用 AI 解决方案自动化客户支持
预算：有 5 万到 10 万美金的预算
时间线：希望在下个季度内实施
备注：目前正在使用竞争对手产品但不满意
```

### 不合格线索示例：

```
线索信息：
姓名：John Doe
邮箱：john@gmail.com
兴趣：可能对 AI 有兴趣
备注：在会议上见面，看起来感兴趣但需求模糊
```

## 顺序代理与其他工作流代理的比较

ADK 提供了不同类型的工作流代理以满足不同需求：

* **顺序代理（Sequential Agents）**：适合严格顺序执行（如本示例）
* **循环代理（Loop Agents）**：根据条件重复执行子代理
* **并行代理（Parallel Agents）**：并发执行相互独立的子代理

## 相关资源

* [ADK 顺序代理官方文档](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/)
* [完整代码开发流水线示例](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/#full-example-code-development-pipeline)

---


