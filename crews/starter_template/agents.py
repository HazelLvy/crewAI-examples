"""
AI 代理定义文件 (Agents)
========================
本文件定义了项目中使用的所有 AI 代理（Agent）。

什么是 Agent（代理）？
----------------------
Agent 是 CrewAI 中的核心概念，代表一个具有特定角色的 AI 助手。
每个 Agent 拥有：
- role（角色）：如"研究员"、"作家"、"分析师"
- goal（目标）：该代理要达成的目标
- backstory（背景故事）：代理的 persona/人设，影响其行为方式
- tools（工具）：可用的工具，如搜索、代码执行等
- llm（语言模型）：驱动代理的底层模型

设计原则：
- 一个 Agent 应专注于某一类工作
- 通过角色设定让 Agent 的输出更符合预期
- Agent 之间通过任务协作完成复杂工作流
"""

from crewai import Agent
# 从环境变量加载配置
from decouple import config

# 导入搜索工具 - 代理可使用此工具进行网络搜索
from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()


class CustomAgents:
    """
    自定义代理工厂类
    ================
    
    使用工厂模式创建和管理所有代理。
    每个方法返回一个配置好的 Agent 实例。
    
    扩展方式：
    如需添加新代理，只需在此类中新增方法即可。
    """
    
    def agent_1_name(self):
        """
        创建第一个代理示例
        
        这是一个研究型代理的模板，你可以根据需要修改：
        - role: 定义代理的角色定位
        - goal: 定义代理的工作目标  
        - backstory: 给代理设定人设，使其输出更自然
        - tools: 提供可用的工具列表
        - verbose: 是否显示详细思考过程
        - allow_delegation: 是否允许将子任务委派给其他代理
        
        返回:
            Agent: 配置好的 CrewAI 代理实例
        """
        return Agent(
            # === 角色定义 ===
            role="在这里定义你的代理角色",           # 例如："高级研究员"
            goal="在这里定义你的代理目标",             # 例如："发现最新信息并提供全面分析"
            
            # === 背景故事/人设 ===
            # 这决定了代理的"性格"和回答风格
            backstory="""在这里定义你的代理背景故事。
            你是一个专家级的代理，拥有丰富的经验和深厚的专业知识。""",
            
            # === 工具配置 ===
            # 代理可以使用这些工具来完成任务
            # 常用工具：搜索工具、API 工具、计算器、代码解释器等
            tools=[search_tool],
            
            # === 行为控制 ===
            verbose=True,              # True: 显示详细日志；False: 静默模式
            
            # === 委派权限 ===
            # True: 代理可以将部分工作分配给其他代理
            # False: 代理必须独立完成所有工作
            allow_delegation=False,
        )

    def agent_2_name(self):
        """
        创建第二个代理示例
        
        与 agent_1 不同，这个代理没有搜索工具，
        更适合做分析、总结、创作等工作。
        
        你可以根据实际需求为不同代理配置不同的能力。
        
        返回:
            Agent: 配置好的 CrewAI 代理实例
        """
        return Agent(
            role="在这里定义你的代理角色",
            goal="在这里定义你的代理目标",
            backstory="""在这里定义你的代理背景故事。
            你是一个经验丰富的代理，擅长处理复杂的分析和创作任务。""",

            # 此代理不使用任何工具，完全依赖其知识能力
            tools=[],
            
            verbose=True,
            allow_delegation=False,
        )
