# CrewAI 入门模板 (Starter Template)

## 项目简介
这是一个 **CrewAI 框架的最小化入门模板**，帮助你快速理解 CrewAI 的核心概念和工作流程。

### 什么是 CrewAI？
CrewAI 是一个用于编排**自主 AI 代理（Agents）**的 Python 框架。它让多个 AI 代理像团队一样协作，共同完成复杂任务。

---

## 📁 文件结构说明

```
starter_template/
├── main.py       # 主程序 - 团队的编排和执行入口
├── agents.py     # 代理定义 - 定义 AI 角色及其能力
├── tasks.py      # 任务定义 - 定义具体的工作内容和要求
├── .env_example  # 环境变量模板 - 需要复制为 .env 并填写
└── README.md     # 本说明文件
```

---

## 🤖 核心概念

| 概念 | 说明 | 类比 |
|------|------|------|
| **Agent（代理）** | 具有角色、目标和背景设定的 AI 助手 | 公司员工 |
| **Task（任务）** | 代理需要完成的具体工作项 | 工作任务 |
| **Crew（团队）** | 将多个代理和任务组织在一起 | 项目组 |
| **Tool（工具）** | 代理可使用的功能，如搜索、计算 | 员工的工具/软件 |

---

## 🚀 快速开始

### 第一步：安装依赖
```bash
pip install crewai langchain-openai python-decouple duckduckgo-search
```

### 第二步：配置环境变量
```bash
# 复制环境变量模板
cp .env_example .env

# 编辑 .env 文件，填入你的 OpenAI API 密钥：
# OPENAI_API_KEY=sk-your-api-key-here
# OPENAI_ORGANIZATION_ID=org-your-org-id
```

### 第三步：运行程序
```bash
python main.py
```

然后按提示输入变量即可看到 AI 团队协作的结果！

---

## 🔄 工作流程图

```
用户输入 → CustomCrew 初始化
              ↓
         创建 Agents（代理）
         ┌─────────┬─────────┐
         │ Agent_1 │ Agent_2 │
         │(研究型) │ (分析型)│
         └────┬────┴────┬────┘
              ↓         ↓
         创建 Tasks（任务）
         ┌─────────┬─────────┐
         │ Task_1  │ Task_2  │
         │(收集信息)│ (分析总结)│
         └────┬────┴────┘
              ↓
         组建 Crew（团队）
              ↓
         kickoff() 执行 → 输出结果
```

---

## 📝 如何自定义

### 1. 添加新代理 (`agents.py`)
```python
def my_new_agent(self):
    return Agent(
        role="数据分析师",                    # 角色
        goal="分析数据并提供洞察",             # 目标
        backstory="你是一位资深的数据科学家...", # 人设
        tools=[some_tool],                   # 可用工具
    )
```

### 2. 添加新任务 (`tasks.py`)
```python
def my_new_task(self, agent):
    return Task(
        description="分析以下数据...",        # 任务描述
        expected_output="分析报告",            # 预期输出格式
        agent=agent,                         # 执行者
    )
```

### 3. 在主程序中注册 (`main.py`)
在 `CustomCrew.run()` 方法中添加你的新代理和新任务即可。

---

## 💡 最佳实践

1. **代理角色要具体** - "高级 Python 研究员" 比 "程序员" 更好
2. **任务描述要清晰** - 包含输入、输出、格式要求
3. **合理使用工具** - 不是所有代理都需要搜索等外部工具
4. **控制委派权限** - `allow_delegation=False` 可防止无限循环
5. **利用上下文链** - 通过 `context` 参数连接前后任务

---

## 🔗 相关资源

- [CrewAI 官方文档](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI 社区](https://community.crewai.com)

## 📄 许可证
MIT License
