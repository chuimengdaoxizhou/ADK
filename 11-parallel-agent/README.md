# ADK 中的并行代理（Parallel Agents）

本示例展示了如何在 Agent Development Kit（ADK）中实现一个并行代理。示例中的主代理为 `system_monitor_agent`，它使用并行代理来同时收集系统信息，并将这些信息整合成一份全面的系统健康报告。

## 什么是并行代理？

并行代理是 ADK 中的一种工作流代理，具有以下特点：

1. **并发执行**：子代理会同时运行，而不是依次执行
2. **独立运行**：每个子代理在执行过程中互不干扰、不共享状态
3. **提高性能**：适合可并行处理的任务，能显著提升效率

当你需要高效地执行多个彼此独立的任务，且时间是关键因素时，应使用并行代理。

## 系统监控示例

本示例构建了一个系统监控应用，利用并行代理来收集系统信息。工作流程包括：

1. **系统信息并行收集**：使用 `ParallelAgent` 并发收集以下信息：

   * CPU 使用情况与统计数据
   * 内存使用情况
   * 磁盘空间与使用情况

2. **系统报告生成（顺序执行）**：并行收集完成后，由一个合成代理生成完整的系统健康报告

### 子代理说明

1. **CPU 信息代理**：收集和分析 CPU 数据

   * 获取核心数、使用率、性能指标
   * 检测高 CPU 使用率等性能问题

2. **内存信息代理**：收集内存使用情况

   * 包括总内存、已用内存、可用内存
   * 分析内存压力、交换分区使用情况

3. **磁盘信息代理**：分析磁盘使用情况

   * 报告总空间、已用空间、可用空间
   * 检测磁盘空间是否即将耗尽

4. **系统报告合成器**：整合所有信息生成系统健康报告

   * 创建系统运行状况的总结
   * 将各部分信息分类整理
   * 根据数据给出优化建议

### 工作流程说明

整个架构结合了并行和顺序两种工作流模式：

1. 首先，`system_info_gatherer` 并行代理同时运行三个信息收集代理
2. 然后，`system_report_synthesizer` 代理使用收集到的数据生成最终报告

这种混合工作流模式展示了如何将多种代理类型组合，实现逻辑清晰且高效的工作流。

## 项目结构

```
10-parallel-agent/
│
├── system_monitor_agent/           # 主代理包
│   ├── __init__.py                 # 包初始化
│   ├── agent.py                    # 根代理定义
│   │
│   └── subagents/                  # 子代理目录
│       ├── __init__.py
│       │
│       ├── cpu_info_agent/         # CPU 信息代理
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── tools.py            # CPU 信息收集工具
│       │
│       ├── memory_info_agent/      # 内存信息代理
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── tools.py            # 内存信息收集工具
│       │
│       ├── disk_info_agent/        # 磁盘信息代理
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── tools.py            # 磁盘信息收集工具
│       │
│       └── synthesizer_agent/      # 报告生成代理
│           ├── __init__.py
│           └── agent.py
│
├── .env.example                    # 环境变量示例文件
└── README.md                       # 本文档
```

## 快速开始

### 设置环境

1. 从根目录激活虚拟环境：

```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. 复制 `.env.example` 为 `.env` 并添加你的 Google API 密钥：

```
GOOGLE_API_KEY=your_api_key_here
```

### 运行示例

```bash
cd 10-parallel-agent
adk web
```

然后在 Web UI 中选择 “system\_monitor\_agent” 即可。

## 示例交互

尝试以下提示词：

```
检查我的系统健康状态
```

```
提供一份完整的系统报告和建议
```

```
我的系统是否内存或磁盘快用完了？
```

## 关键概念：独立执行

并行代理的一个关键特点是 **子代理在执行时互不共享状态**。在本示例中：

1. 每个信息收集代理在独立环境中运行
2. 并行执行完成后，再统一收集所有结果
3. 最后由合成代理基于这些数据生成最终报告

这种方式非常适合任务完全独立、无需交互的场景。

## 并行代理与其他工作流代理的比较

ADK 提供多种工作流代理，适配不同需求：

* **顺序代理（Sequential Agents）**：适合严格的顺序执行，前一步输出作为后一步输入
* **循环代理（Loop Agents）**：用于根据条件反复执行子代理
* **并行代理（Parallel Agents）**：适合同时执行多个独立子任务（如本示例）

## 相关资源

* [ADK 并行代理文档（英文）](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
* [完整示例：并行网页研究](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/#full-example-parallel-web-research)

---

