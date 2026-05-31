"""
CrewAI 入门模板 - 主程序文件
============================
这是项目的入口点，负责：
1. 初始化 AI 代理（Agents）和任务（Tasks）
2. 组建团队（Crew）并执行工作流程
3. 接收用户输入并输出最终结果
"""

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
# python-decouple: 用于从 .env 文件安全地读取环境变量
from decouple import config

# dedent: 用于去除多行字符串的缩进，使输出格式更整洁
from textwrap import dedent

# 导入自定义的代理和任务类
from agents import CustomAgents
from tasks import CustomTasks

# 安装 DuckDuckGo 搜索工具（用于本示例中的网络搜索功能）
# !pip install -U duckduckgo-search
from langchain.tools import DuckDuckGoSearchRun

# 创建搜索工具实例，可供代理使用来获取实时信息
search_tool = DuckDuckGoSearchRun()

# 从环境变量加载 OpenAI API 密钥和组织 ID
os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
os.environ["OPENAI_ORGANIZATION"] = config("OPENAI_ORGANIZATION_ID")


class CustomCrew:
    """
    自定义团队类（核心编排器）
    ==========================
    职责：
    - 将多个 AI 代理和任务组合成一个协作团队
    - 管理团队的工作流程执行
    - 处理用户输入并返回结果
    
    使用方式：
    1. 实例化时传入变量（如用户输入的主题、参数等）
    2. 调用 run() 方法启动团队执行任务
    """
    
    def __init__(self, var1, var2):
        """
        初始化团队，接收用户传入的变量
        
        参数:
            var1: 用户输入的第一个变量（可自定义用途，如搜索主题）
            var2: 用户输入的第二个变量
        """
        self.var1 = var1
        self.var2 = var2

    def run(self):
        """
        执行团队工作流程
        
        流程说明：
        1. 创建代理实例和任务实例
        2. 定义具体的代理（Agent）- 每个 Agent 有特定的角色和能力
        3. 定义具体任务（Task）- 每个任务分配给对应的代理执行
        4. 组建团队并运行（kickoff）
        
        返回:
            result: 团队执行后的最终输出结果
        """
        
        # === 第一步：初始化代理工厂和任务工厂 ===
        # CustomAgents: 用于创建各种 AI 代理
        # CustomTasks: 用于创建各种任务
        agents = CustomAgents()
        tasks = CustomTasks()

        # === 第二步：定义 AI 代理 ===
        # 代理是具有特定角色、目标和背景设定的 AI 角色
        custom_agent_1 = agents.agent_1_name()
        custom_agent_2 = agents.agent_2_name()

        # === 第三步：定义任务 ===
        # 任务是代理需要完成的具体工作，包含描述、预期输出等
        # 注意：任务需要指定由哪个代理执行，并可传入变量作为上下文
        
        # 任务1：由 agent_1 执行，接收 var1 和 var2 作为输入
        custom_task_1 = tasks.task_1_name(
            custom_agent_1,  # 指定执行此任务的代理
            self.var1,       # 用户传入的变量1
            self.var2,       # 用户传入的变量2
        )

        # 任务2：由 agent_2 执行
        custom_task_2 = tasks.task_2_name(
            custom_agent_2,  # 指定执行此任务的代理
        )

        # === 第四步：组建团队并执行 ===
        # Crew 是 CrewAI 的核心概念，将代理和任务组织在一起
        # Process 默认为顺序执行（Sequential），也可设置为并行（Parallel）
        crew = Crew(
            agents=[custom_agent_1, custom_agent_2],  # 参与团队的代理列表
            tasks=[custom_task_1, custom_task_2],     # 需要完成的任务列表
            verbose=True,                              # 是否显示详细执行日志
        )

        # kickoff(): 启动团队，开始执行所有任务
        result = crew.kickoff()
        return result


# ==================== 程序入口 ====================
if __name__ == "__main__":
    print("## Welcome to Crew AI Template")   # 欢迎信息
    print("-------------------------------")
    
    # 从命令行获取用户输入
    # dedent 使多行字符串格式化更美观
    var1 = input(dedent("""Enter variable 1: """))  # 输入第一个变量
    var2 = input(dedent("""Enter variable 2: """))  # 输入第二个变量

    # 创建自定义团队实例并运行
    custom_crew = CustomCrew(var1, var2)
    result = custom_crew.run()
    
    # 打印最终结果
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)
