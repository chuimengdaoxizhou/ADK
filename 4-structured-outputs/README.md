# ADK中的结构化输出示例

本示例展示了如何在Agent Development Kit（ADK）中使用Pydantic模型实现结构化输出。示例中的主Agent `email_generator` 使用 `output_schema` 参数，确保其响应符合特定的结构化格式。

## 什么是结构化输出？

ADK允许你使用Pydantic模型定义Agent输入和输出的结构化数据格式：

1. **输出格式可控**：使用 `output_schema` 确保LLM生成的响应具有一致的JSON结构
2. **数据验证**：Pydantic会验证所有必填字段是否存在且格式正确
3. **下游处理更简便**：结构化输出更易于被后续应用或其他Agent处理

当你需要保证与其他系统或Agent集成时输出格式一致，建议使用结构化输出。

## 邮件生成器示例

本示例创建了一个邮件生成Agent，其结构化输出包括：

1. **邮件主题**：简明且相关的主题行
2. **邮件正文**：格式良好的邮件内容，包含问候语、段落和签名

Agent使用名为 `EmailContent` 的Pydantic模型定义结构，确保每次响应都符合相同格式。

### 输出结构定义

Pydantic模型明确规定了所需字段及其说明：

```python
class EmailContent(BaseModel):
    """邮件内容结构，包含主题和正文。"""
    
    subject: str = Field(
        description="邮件主题，简洁且描述性强。"
    )
    body: str = Field(
        description="邮件正文，格式良好，包含问候、段落和签名。"
    )
```

### 工作流程

1. 用户提供邮件需求描述
2. LLM Agent处理请求，生成主题和正文
3. Agent将响应格式化为符合 `EmailContent` 结构的JSON
4. ADK根据结构校验响应
5. 结构化结果存储于会话状态指定的 `output_key` 中

## 重要限制

使用 `output_schema` 时：

1. **不支持工具调用**：带有输出结构的Agent执行时不能调用工具
2. **必须直接返回JSON**：LLM最终输出必须是符合结构的JSON
3. **需明确指示**：Agent指令要明确引导LLM生成正确格式的JSON

## 项目结构

```
4-structured-outputs/
│
├── email_agent/                   # 邮件生成Agent包
│   └── agent.py                   # 带输出结构的Agent定义
│
└── README.md                      # 本文档
```

## 开始使用

### 环境准备

1. 从项目根目录激活虚拟环境：

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 创建 `.env` 文件并添加你的Google API密钥：

```
GOOGLE_API_KEY=your_api_key_here
```

### 运行示例

```bash
cd 4-structured-outputs
adk web
```

然后在Web UI中选择 `email_generator` 运行。

## 示例交互

尝试以下示例提示：

```
给我的团队写一封专业邮件，说明项目截止日期延长两周。
```

```
给客户起草一封邮件，解释我们需要更多信息才能继续处理订单。
```

```
安排与市场部门的会议，讨论新产品发布策略。
```

## 关键概念：结构化数据交换

结构化输出是ADK支持结构化数据交换的一部分，包括：

1. **input\_schema**：定义期望的输入格式（本例未使用）
2. **output\_schema**：定义所需的输出格式（本例使用）
3. **output\_key**：将结果存储于会话状态，供其他Agent使用（本例使用）

此设计模式保证了Agent之间以及与外部系统的数据交互格式可靠。

## 额外资源

* [ADK结构化数据文档](https://google.github.io/adk-docs/agents/llm-agents/#structuring-data-input_schema-output_schema-output_key)
* [Pydantic文档](https://docs.pydantic.dev/latest/)
  
  


