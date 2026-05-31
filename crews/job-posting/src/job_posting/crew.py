"""
职位发布生成器 - 核心编排文件 (Core Orchestration)
====================================================
本文件是职位描述（Job Posting）生成系统的核心，负责：

1. 从 YAML 配置文件加载代理和任务定义
2. 定义 3 个专业代理的配置和工具
3. 定义 5 个任务的依赖关系
4. 组建团队并协调执行

工作流程：
  公司文化研究 → 行业分析 → 岗位要求研究
    → 起草职位描述 → 审核与修改

团队组成（3 个代理）：
┌───────────────────────────────────────────────┐
│  research_agent   - 研究员：调研公司和行业信息     │
│  writer_agent     - 撰稿人：撰写职位描述文档      │
│  review_agent     - 审核员：审核和优化内容        │
└───────────────────────────────────────────────┘

架构说明：
本示例使用 CrewAI 的 @CrewBase 装饰器模式，
通过 YAML 配置 + Python 代码结合的方式定义代理和任务。
这是一种比纯代码方式更简洁、更易维护的写法。
"""

from typing import List
# CrewAI 核心组件：Agent（代理）、Crew（团队）、Task（任务）、Process（流程模式）
from crewai import Agent, Crew, Process, Task
# @CrewBase / @agent / @task / @crew：装饰器模式的基类和装饰器
from crewai.project import CrewBase, agent, crew, task

# 导入 CrewAI 内置工具（预封装好的常用工具）
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool, FileReadTool
# Pydantic: 用于定义结构化数据模型（确保输出格式规范）
from pydantic import BaseModel, Field


# ==================== 工具实例化 ====================

# 网站搜索工具 — 在指定网站上搜索特定内容
# 用途：在公司官网上搜索相关信息，了解公司业务和文化
web_search_tool = WebsiteSearchTool()

# Serper Dev 搜索工具 — 通过 Google 搜索引擎获取实时信息
# 用途：搜索行业标准 JD 格式、类似职位的描述、行业术语等
seper_dev_tool = SerperDevTool()

# 文件读取工具 — 读取本地文件内容
# 用途：读取示例职位描述文件 (job_description_example.md) 作为参考模板
file_read_tool = FileReadTool(
    file_path='job_description_example.md',
    description='A tool to read the job description example file.'
)


# ==================== 数据模型定义 ====================

class ResearchRoleRequirements(BaseModel):
    """
    岗位要求数据模型（Pydantic 模型）
    ==================================
    
    用于约束"研究岗位要求"任务的输出格式。
    使用 Pydantic BaseModel 可以确保输出是结构化的 JSON 数据，
    而非自由格式的文本。这对于后续任务引用非常方便。
    
    为什么需要数据模型？
    ────────────────────
    - 强制输出为固定格式，避免遗漏关键字段
    - 后续任务可以按字段精确引用（如 {output.skills}）
    - 提高整个流水线的一致性和可靠性
    
    字段说明:
        skills:     候选人应具备的技能列表（如 "Python", "项目管理"）
        experience: 期望的工作经验（如 "3年以上影视制作经验"）
        qualities:  期望的个人品质（如 "良好的沟通能力", "注重细节"）
    """
    """Research role requirements model"""
    skills: List[str] = Field(
        ..., 
        description="List of recommended skills for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements."
        # 推荐技能列表 — 需与公司文化、正在进行的项目以及该具体岗位的要求相匹配
    )
    experience: List[str] = Field(
        ..., 
        description="List of recommended experience for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements."
        # 推荐经验列表 — 包括工作年限、相关项目经验等
    )
    qualities: List[str] = Field(
        ..., 
        description="List of recommended qualities for the ideal candidate aligned with the company's culture, ongoing projects, and the specific role's requirements."
        # 推荐品质列表 — 如软技能、性格特点等
    )


# ==================== 团队类定义 ====================

@CrewBase  # ⭐ CrewAI 项目基类装饰器 —— 启用 YAML 配置自动加载功能
class JobPostingCrew:
    """
    职位发布团队类
    =============
    
    继承自 CrewBase，使用装饰器模式管理代理和任务。
    
    配置来源:
        agents_config: 'config/agents.yaml'  ← 代理的角色/目标/背景设定
        tasks_config:  'config/tasks.yaml'   ← 任务的描述/预期输出
    
    @CrewBase 的优势:
        - 自动从 YAML 文件加载配置（无需手动 yaml.safe_load）
        - 自动收集所有 @agent 和 @task 装饰的方法
        - self.agents 和 self.tasks 属性自动可用
        - 支持训练模式 (train 方法)
    """
    """JobPosting crew"""
    
    # 配置文件路径（相对于 crew.py 所在目录）
    agents_config = 'config/agents.yaml'   # 代理配置
    tasks_config = 'config/tasks.yaml'     # 任务配置

    # ================================================================
    #                      代理定义 (Agents)
    #   使用 @agent 裂饰器 —— CrewBase 会自动收集这些方法作为代理
    # ================================================================

    @agent
    def research_agent(self) -> Agent:
        """
        研究员代理
        
        职责：
        - 调研公司文化和价值观（从官网抓取信息）
        - 分析该职位在行业中的标准要求和薪酬范围
        - 收集类似职位的描述参考
        
        工具：
        - web_search_tool: 在公司网站内搜索
        - seper_dev_tool: Google 搜索行业信息
        """
        return Agent(
            config=self.agents_config['research_agent'],  # 从 YAML 加载配置
            tools=[web_search_tool, seper_dev_tool],
            verbose=True
        )
    
    @agent
    def writer_agent(self) -> Agent:
        """
        撰稿人代理
        
        职责：
        - 根据研究结果起草完整的职位描述
        - 确保文案风格专业且有吸引力
        - 参考示例文件的格式和结构
        
        工具：
        - web_search_tool: 补充搜索需要的术语或表达
        - seper_dev_tool: 查找最佳实践参考
        - file_read_tool: 读取示例 JD 作为格式参考 ⭐ 关键
        """
        return Agent(
            config=self.agents_config['writer_agent'],
            tools=[web_search_tool, seper_dev_tool, file_read_tool],
            verbose=True
        )
    
    @agent
    def review_agent(self) -> Agent:
        """
        审核代理
        
        职责：
        - 审查草稿的完整性和准确性
        - 检查是否符合公司品牌调性
        - 提出改进建议并优化最终版本
        - 充当质量控制角色（QA）
        
        工具：
        - web_search_tool: 对比同类公司的 JD 质量
        - seper_dev_tool: 查找 JD 最佳实践标准
        - file_read_tool: 对照原始示例检查格式一致性
        """
        return Agent(
            config=self.agents_config['review_agent'],
            tools=[web_search_tool, seper_dev_tool, file_read_tool],
            verbose=True
        )
    
    # ================================================================
    #                      任务定义 (Tasks)
    #   使用 @task 装饰器 —— CrewBase 会自动收集这些方法作为任务
    # ================================================================

    @task
    def research_company_culture_task(self) -> Task:
        """
        任务1：研究公司文化
        
        执行者：research_agent（研究员）
        目标：深入了解公司的使命、价值观、文化和工作环境
        输出：公司文化分析报告（文本形式）
        位置：流水线的第一个任务，为后续任务提供基础信息
        """
        return Task(
            config=self.tasks_config['research_company_culture_task'],
            agent=self.research_agent()
        )

    @task
    def research_role_requirements_task(self) -> Task:
        """
        任务2：研究岗位要求
        
        执行者：research_agent（研究员）
        目标：确定该职位所需的具体技能、经验和素质
        输出：结构化的 ResearchRoleRequirements 模型（JSON 格式）
        
        特殊之处：
        - 使用 output_json=ResearchRoleRequirements 输出结构化数据
        - 这让后续撰稿人任务可以精确引用各个字段
        - 例如：{skills}, {experience}, {qualities}
        """
        return Task(
            config=self.tasks_config['research_role_requirements_task'],
            agent=self.research_agent(),
            output_json=ResearchRoleRequirements  # ⭐ 输出为结构化 JSON
        )

    @task
    def draft_job_posting_task(self) -> Task:
        """
        任务3：起草职位描述
        
        执行者：writer_agent（撰稿人）
        目标：综合前面所有研究成果，撰写完整的职位描述草稿
        输出：完整的 JD 文档（Markdown/文本格式）
        
        这是核心创作任务——将研究和分析转化为实际可用的招聘文案。
        """
        return Task(
            config=self.tasks_config['draft_job_posting_task'],
            agent=self.writer_agent()
        )

    @task
    def review_and_edit_job_posting_task(self) -> Task:
        """
        任务4：审核并编辑职位描述（最终任务）
        
        执行者：review_agent（审核员）
        目标：审查草稿质量并进行必要的编辑和优化
        输出：经过审核的最终版职位描述
        
        这是最后一个任务——确保交付给用户的 JD 是高质量的。
        """
        return Task(
            config=self.tasks_config['review_and_edit_job_posting_task'],
            agent=self.review_agent()
        )

    @task
    def industry_analysis_task(self) -> Task:
        """
        任务5（可选）：行业分析
        
        执行者：research_agent（研究员）
        目标：分析该职位所在行业的整体趋势、薪资水平和竞争格局
        输出：行业分析报告
        
        注意：
        此任务与其他任务是并行关系还是顺序关系取决于 YAML 中的 context 设置。
        通常用于补充市场上下文，使 JD 更有竞争力。
        """
        return Task(
            config=self.tasks_config['industry_analysis_task'],
            agent=self.research_agent()
        )

    # ================================================================
    #                        组建团队 (Crew)
    #   使用 @crew 装饰器 —— 定义如何将代理和任务组合成完整团队
    # ================================================================

    @crew
    def crew(self) -> Crew:
        """
        创建职位发布团队实例
        
        返回一个配置好的 Crew 对象，包含：
        - 所有已注册的代理（由 @agent 装饰器自动收集）
        - 所有已注册的任务（由 @task 装饰器自动收集）
        - 顺序执行模式（Process.sequential）
        - 详细日志输出（verbose=2）
        """
        """Creates the JobPostingCrew"""
        return Crew(
            agents=self.agents,  # 由 @agent 装饰器自动收集的所有代理
            tasks=self.tasks,    # 由 @task 装饰器自动收集的所有任务
            process=Process.sequential,  # 顺序执行模式（任务依次完成）
            verbose=2,                   # 最详细的日志级别（显示每个步骤）
        )
