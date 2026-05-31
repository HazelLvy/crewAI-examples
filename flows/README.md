# CrewAI Flows 示例集

本目录包含展示 **CrewAI Flows 模式**的示例 —— 这是一个强大的编排框架，用于管理**复杂的多团队（multi-crew）工作流**，支持状态管理。

## 什么是 CrewAI Flows？

CrewAI Flows 允许你：
- **按顺序或并行**编排多个团队（Crew）
- 在不同的执行步骤之间**管理和传递状态**
- 实现**条件逻辑和动态路由**
- 创建**人工在环（Human-in-the-Loop）**工作流
- 构建复杂的**自动化流水线**

## 本目录中的示例

### 1. Content Creator Flow（内容创作流程）
多团队内容生成系统，功能包括：
- 将请求**路由分发**到专业团队（博客、LinkedIn、研究报告）
- 跨不同格式生成**专业化内容**
- 使用**动态路由**的高级编排能力
- 展示复杂的多代理工作流

### 2. Email Auto Responder Flow（邮件自动回复流程）
自动化邮件监控与回复生成系统，功能包括：
- 定期**监控 Gmail 收件箱**
- **过滤和分类** incoming 邮件
- 生成适当的**草稿回复**
- 维护已处理邮件的**状态记录**

### 3. Lead Score Flow（销售线索评分流程）
销售线索资格评估和外联自动化，功能包括：
- 从 **CSV 文件**处理销售线索
- 基于标准对线索进行**评分和排名**
- 对高分候选人实施**人工审核环节**
- 生成**个性化的外联邮件**

### 4. Meeting Assistant Flow（会议助手流程）
会议生产力自动化系统，功能包括：
- 处理会议**转录文本和笔记**
- **提取待办事项（Action Items）和决议**
- 在 **Trello** 中自动创建任务卡片
- 通过 **Slack** 发送通知

### 5. Self Evaluation Loop Flow（自评循环流程）
迭代式内容改进系统，功能包括：
- 生成内容（如社交媒体帖子）
- 对照标准进行**自我评估**
- 根据反馈**自动优化改进**
- 实现带**重试限制**的重试逻辑

### 6. Write a Book with Flows（使用 Flows 写书）
书籍创作自动化系统，功能包括：
- 生成**书籍大纲**
- **并行撰写**各章节
- 保持各章节之间的**一致性**
- 汇编最终**完整手稿**

## 常见的 Flow 模式

### 顺序执行
```python
# 让团队一个接一个地执行
flow = Flow()
flow.add_crew(crew1)
flow.add_crew(crew2)
```

### 并行执行
```python
# 同时执行多个团队
await flow.run_parallel([crew1, crew2, crew3])
```

### 条件路由
```python
# 根据前面的结果决定后续路径
@flow.router
def route_based_on_result(state):
    if state.score > 0.8:
        return "high_quality_path"     # 高质量 → 走高质量路径
    return "needs_improvement_path"    # 不合格 → 走改进路径
```

### 人工在环（Human-in-the-Loop）
```python
# 暂停等待人类输入
human_feedback = flow.wait_for_input("Review these results")
```

## 快速开始

每个示例都包含：
- 完整的可运行代码
- 配置文件
- 附带具体说明的 README 文件
- 所需的依赖项

选择一个与你需求匹配的示例，然后按照其 README 中的说明进行设置即可。
