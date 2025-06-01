以下是该 LiteLLM Agent 示例文档的完整中文翻译：

---

# LiteLLM Agent 示例

## 什么是 LiteLLM？

LiteLLM 是一个 Python 库，提供了一个统一的接口，让你可以通过一致的 API 与多个大语言模型（LLM）提供商交互。它本质上是一个适配器，具备以下功能：

* 用相同的代码访问 100 多个来自不同提供商（如 OpenAI、Anthropic、Google、AWS Bedrock 等）的模型
* 标准化不同模型的输入和输出格式
* 统一跟踪费用、管理 API 密钥、处理错误
* 支持模型的自动降级、负载均衡等机制

简而言之，LiteLLM 就像一个统一封装器，让你可以轻松在不同 LLM 之间切换，无需修改应用代码。

---

## 为什么要在 ADK 中使用 LiteLLM？

Google 的 ADK（Agent Development Kit）是一个模型无关的平台，理论上可以与多种 LLM 提供商配合使用。LiteLLM 可以进一步增强这一能力，其优势包括：

1. **模型提供商灵活性**：轻松在 OpenAI、Anthropic 等不同提供商之间切换
2. **成本优化**：选择性价比最高的模型以降低成本
3. **快速试验新模型**：快速切换模型，探索最适合你任务的选项
4. **面向未来**：新模型发布时可快速集成，无需重写大量代码

本示例演示如何使用 LiteLLM 与 ADK 结合，使用 OpenRouter 接入非 Google 模型，如 Anthropic 的 Claude 3.5 Sonnet，而不是默认的 Gemini。

---

## 使用非 Google 模型时的限制

当你通过 LiteLLM 使用非 Google 模型接入 ADK 时，请注意以下限制：

1. **无法使用 Google 内置工具**：
   非 Google 模型（如 OpenAI、Anthropic 等）**无法使用 ADK 的内置 Google 工具**，例如：

   * Google Search（谷歌搜索）
   * Code Execution（代码执行）
   * Vertex AI Search（谷歌 AI 搜索）

2. **只能使用自定义函数工具（Function Tool）**：
   使用非 Google 模型时，只能通过自定义函数构建工具，例如本示例中的 `get_dad_joke()`。

这些限制的原因是内置工具依赖 Google 的模型与基础设施，只能在 Gemini 系列模型中使用。但你仍可以通过自定义工具 + 第三方模型构建功能强大的 Agent。

---

## 快速开始

该示例使用的是 ADK 根目录下创建的虚拟环境。请确保：

1. 已激活虚拟环境：

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 配置好 OpenRouter API 密钥：

   * 注册 [OpenRouter](https://openrouter.ai/) 账号
   * 访问 [https://openrouter.ai/keys](https://openrouter.ai/keys) 获取 API Key
   * 将 `openrouter_dad_joke_agent` 文件夹下的 `.env.example` 重命名为 `.env`
   * 将你的 OpenRouter 密钥填入 `.env` 文件中的 `OPENROUTER_API_KEY`

---

## 示例说明

此示例演示了以下内容：

1. 如何使用 ADK 中的 `LiteLlm` 模型适配器
2. 如何通过 OpenRouter 接入第三方模型（如 Claude 3.5 Sonnet）
3. 如何创建一个带自定义函数的简单 Agent

这个 Agent 通过调用自定义函数 `get_dad_joke()` 来讲“爸爸笑话”，使用的是 Anthropic 的 Claude 3.5 Sonnet 模型，通过 OpenRouter 接入，而非 Google 的 Gemini。

---

## 运行示例

1. 进入 `3-litellm-agent` 目录，包含你的 agent 文件夹
2. 启动交互式 Web UI：

```bash
adk web
```

3. 打开终端中显示的链接（通常是 [http://localhost:8000）访问](http://localhost:8000）访问) Web UI
4. 在左上角下拉框中选择 `openrouter_dad_joke_agent`
5. 在底部输入框中与你的 Agent 聊天

### 示例提示词：

* “Tell me a dad joke”（讲个爸爸笑话）

按 `Ctrl+C` 可在终端中退出会话或停止服务。

---

## 修改模型的方式

你可以非常方便地修改此示例中的模型配置，只需更改 `LiteLlm` 的 model 字符串即可：

```python
# 使用 Claude 3.5 Sonnet（Anthropic）通过 OpenRouter
model = LiteLlm(
    model="openrouter/anthropic/claude-3-5-sonnet",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# 使用 GPT-4o（OpenAI）通过 OpenRouter
model = LiteLlm(
    model="openrouter/openai/gpt-4o",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# 使用 Llama 3 70B（Meta）通过 OpenRouter
model = LiteLlm(
    model="openrouter/meta-llama/meta-llama-3-70b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# 使用 Mistral Large 通过 OpenRouter
model = LiteLlm(
    model="openrouter/mistral/mistral-large-latest",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# 使用 Ollama 
# 可用模型示例：llama3, gemma, codellama 等
OLLAMA_MODEL = "llama3"

# 使用 LiteLLM 的 Ollama 模型适配器
model = LiteLlm(
    model=f"ollama/{OLLAMA_MODEL}",
    api_base="http://localhost:11434",  # Ollama 默认端口
)
```

---

## 更多资源

* [Google ADK LiteLLM 集成文档（官方）](https://google.github.io/adk-docs/tutorials/agent-team/#step-2-going-multi-model-with-litellm-optional)
* [LiteLLM 官方文档](https://docs.litellm.ai/docs/)
* [LiteLLM 支持的模型提供商列表](https://docs.litellm.ai/docs/providers)
* [OpenRouter 文档](https://openrouter.ai/docs)
* [Anthropic Claude 模型概览](https://docs.anthropic.com/en/docs/about-claude/models/all-models)

---


