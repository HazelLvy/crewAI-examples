# CrewAI 标准团队示例 (Standard Crews Examples)

本目录包含传统 CrewAI 实现的示例——**自主 AI 代理团队协作完成复杂任务**。

## 什么是 CrewAI 团队（Crew）？

CrewAI 团队是由多个 AI 代理组成的团队，每个代理拥有特定的角色和目标，协同工作以完成任务。核心组件包括：

- **Agents（代理）**：具有特定角色和专业知识的自主 AI 实体
- **Tasks（任务）**：代理需要完成的明确目标
- **Tools（工具）**：代理可以使用的功能和集成
- **Process（流程）**：顺序执行或层级化的任务执行模式

## 本目录中的示例

### 内容创作
- **game-builder-crew**：设计和构建 Python 游戏的多代理团队
- **instagram_post**：结合研究和创意，生成吸引人的 Instagram 内容
- **landing_page_generator**：从概念出发构建完整的落地页
- **marketing_strategy**：制定全面的营销活动方案
- **screenplay_writer**：将文本转换为专业的剧本格式

### 业务与效率
- **job-posting**：分析公司信息并创建定制化的职位描述
- **prep-for-a-meeting**：研究参会人员并准备会议策略
- **recruitment**：自动化候选人搜寻和评估流程
- **stock_analysis**：利用 SEC 数据进行全面金融分析

### 数据与匹配
- **match_profile_to_positions**：使用向量搜索进行简历与岗位匹配
- **meta_quest_knowledge**：基于 PDF 文档的问答系统

### 旅行与规划
- **surprise_trip**：规划个性化的惊喜旅行行程
- **trip_planner**：比较目的地并优化旅行计划

### 模板
- **starter_template**：创建新 CrewAI 项目的基础模板

## 常见团队模式（Patterns）

### 代理定义
```yaml
# agents.yaml
researcher:
  role: "高级研究分析师"
  goal: "发现前沿发展动态"
  backstory: "你是一位经验丰富的研究员..."
```

### 任务定义
```yaml
# tasks.yaml
research_task:
  description: "对 {topic} 进行全面研究"
  agent: researcher
  expected_output: "详细的研究报告"
```

### 组建团队
```python
from crewai import Crew, Agent, Task

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process="sequential"  # 或 "hierarchical"（层级模式）
)
```

## 展示的关键特性

1. **多代理协作**：示例展示了 2-7 个代理协同工作
2. **工具集成**：网页搜索、API 调用、文件操作、数据库访问
3. **自定义工具**：许多示例实现了专用工具
4. **YAML 配置**：标准化的代理/任务定义方式
5. **多领域覆盖**：从创意写作到金融分析，涵盖多种场景

## 快速开始

1. 选择一个与你的需求相匹配的示例
2. 进入对应的目录
3. 阅读该示例的 README 说明文件
4. 安装依赖（通常通过 `pip install -r requirements.txt` 或 `poetry install`）
5. 运行 `python main.py` 或按说明执行

每个示例都是自包含的，包含所有必要的配置，可作为你创建自己的团队的起点。
