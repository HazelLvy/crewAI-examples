# CrewAI 完整示例集

## 简介
欢迎来到 **完整 CrewAI 应用程序** 的官方集合。本仓库包含端到端的实现示例，展示了如何使用 CrewAI 的 AI 代理编排框架构建实际应用程序。

> **🍳 寻找特定功能的教程？** 请查看 [CrewAI Cookbook](https://github.com/crewAIInc/crewAI-cookbook) 获取针对特定 CrewAI 功能和模式的专门指南。

## 你将在这里找到什么

这些是**完整应用程序**，展示以下内容：
- 完整的项目结构和组织方式
- 真实世界的集成模式（API、数据库、外部服务）
- 包含错误处理的完整代码实现
- 从输入到输出的端到端工作流程
- 跨各领域的行业特定实现

每个示例都是可以运行、修改和部署的独立应用程序。

**注意**：所有示例均使用 **CrewAI 版本 0.152.0** 和 **UV 包管理器** 以获得最佳性能和开发体验。

## 📁 仓库结构

### 🌊 [Flows](/flows)
使用 CrewAI Flows 进行高级编排的示例，适用于具有状态管理的复杂工作流程。

- [Content Creator Flow](flows/content_creator_flow) - 多团队内容生成系统，用于博客、LinkedIn 帖子和研究报告
- [Email Auto Responder Flow](flows/email_auto_responder_flow) - 自动化邮件监控和回复生成
- [Lead Score Flow](flows/lead-score-flow) - 带有人工审核环节的销售线索资格评估
- [Meeting Assistant Flow](flows/meeting_assistant_flow) - 集成 Trello/Slack 的会议纪要处理
- [Self Evaluation Loop Flow](flows/self_evaluation_loop_flow) - 带自审机制的迭代式内容改进
- [Write a Book with Flows](flows/write_a_book_with_flows) - 自动化书籍写作，支持并行章节生成

### 👥 [Crews](/crews)
传统的 CrewAI 实现，展示多代理协作模式。

#### 内容创作与营销
- [Game Builder Crew](crews/game-builder-crew) - 设计和构建 Python 游戏的多代理团队
- [Instagram Post](crews/instagram_post) - 创意社交媒体内容生成
- [Landing Page Generator](crews/landing_page_generator) - 从概念到完整落地页的创建
- [Marketing Strategy](crews/marketing_strategy) - 全面的营销活动策划
- [Screenplay Writer](crews/screenplay_writer) - 将文本/邮件转换为剧本格式

#### 业务与效率
- [Job Posting](crews/job-posting) - 自动化职位描述创建
- [Prep for a Meeting](crews/prep-for-a-meeting) - 会议准备研究和策略制定
- [Recruitment](crews/recruitment) - 自动化候选人搜寻和评估
- [Stock Analysis](crews/stock_analysis) - 集成 SEC 数据的金融分析

#### 数据与研究
- [Industry Agents](crews/industry-agents) - 行业特定的代理实现
- [Match Profile to Positions](crews/match_profile_to_positions) - 使用向量搜索进行简历与岗位匹配
- [Meta Quest Knowledge](crews/meta_quest_knowledge) - 基于 PDF 的问答系统
- [Markdown Validator](crews/markdown_validator) - 自动化 Markdown 验证和纠正

#### 旅行与规划
- [Surprise Trip](crews/surprise_trip) - 个性化惊喜旅行规划
- [Trip Planner](crews/trip_planner) - 目的地比较和行程优化

#### 模板
- [Starter Template](crews/starter_template) - 新 CrewAI 项目的基础模板

### 🔌 [Integrations](/integrations)
展示 CrewAI 与其他平台和服务集成的示例。

- [CrewAI-LangGraph](integrations/CrewAI-LangGraph) - 与 LangGraph 框架集成
- [Azure Model](integrations/azure_model) - 在 CrewAI 中使用 Azure OpenAI
- [NVIDIA Models](integrations/nvidia_models) - 与 NVIDIA AI 生态系统集成

### 📓 [Notebooks](/Notebooks)
用于交互式探索和学习的 Jupyter notebook 示例。

## 🚀 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/crewAIInc/crewAI-examples.git
   cd crewAI-examples
   ```

2. **选择示例类别**
   - 多团队编排 → 查看 `/flows`
   - 标准团队 → 查看 `/crews`
   - 平台集成 → 查看 `/integrations`

3. **进入具体示例**
   ```bash
   cd crews/marketing_strategy  # 或任何其他示例
   ```

4. **使用 UV 安装依赖**
   ```bash
   uv sync  # 安装所有依赖并创建虚拟环境
   ```

5. **遵循示例的 README**
   每个示例都包含具体的设置说明和使用指南

## 📚 学习路径

### 初学者
从以下开始：
1. [Starter Template](crews/starter_template) - 基础团队结构
2. [Instagram Post](crews/instagram_post) - 简单的内容创建
3. [Job Posting](crews/job-posting) - 简单的业务用例

### 中级
探索以下内容：
1. [Marketing Strategy](crews/marketing_strategy) - 多代理协作
2. [Self Evaluation Loop Flow](flows/self_evaluation_loop_flow) - 迭代式工作流程
3. [Stock Analysis](crews/stock_analysis) - 外部 API 集成

### 高级
深入学习：
1. [Content Creator Flow](flows/content_creator_flow) - 带动态路由的多团队编排
2. [Write a Book with Flows](flows/write_a_book_with_flows) - 复杂并行执行
3. [Lead Score Flow](flows/lead-score-flow) - 人工在环（Human-in-the-loop）模式
4. [CrewAI-LangGraph](integrations/CrewAI-LangGraph) - 框架集成

## 🛠 常见模式

- **配置**：大多数示例使用 YAML 文件定义代理/任务
- **工具**：示例展示与 API、数据库和文件系统的集成
- **Flows**：高级示例演示状态管理和编排
- **训练**：多个示例包含代理训练功能

## 📝 贡献

我们欢迎贡献！请随时提交展示新用例或改进现有示例的代码。

## 📄 许可证

本仓库由 CrewAI 团队维护。具体许可信息请查看各个示例。

---

## 🔗 相关资源

- **[CrewAI Framework](https://github.com/crewAIInc/crewAI)** - CrewAI 主仓库
- **[CrewAI Cookbooks](https://github.com/crewAIInc/crewAI-cookbook)** - 面向功能的教程和指南
- **[CrewAI Documentation](https://docs.crewai.com)** - 全面文档
- **[CrewAI Community](https://community.crewai.com)** - 加入我们的社区讨论
