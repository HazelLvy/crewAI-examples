"""
落地页生成团队 - 核心编排文件
==============================
本文件是整个落地页生成系统的核心，负责：

1. 加载配置（代理定义、任务定义、模板引用）
2. 创建和管理所有 AI 代理
3. 定义完整的任务流水线
4. 协调代理之间的协作，从"想法"到"完整落地页"

工作流程：
  想法输入 → 分析想法 → 选模板 → 规划内容 → 修改代码 → 生成落地页

输出：完整的 HTML/CSS/JS 文件（打包为 ZIP）
"""

import os
import json
import yaml

from crewai import Agent, Crew, Process, Task

# 导入自定义工具类
from tools.file_tools import FileTools
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from tools.template_tools import TemplateTools


class LandingPageCrew:
    """
    落地页生成器主团队类
    =====================
    
    职责：
    - 读取 YAML 配置文件来初始化代理和任务
    - 管理 5 个专业代理的协作流程
    - 处理模板选择、内容规划、代码修改等全链路
    
    团队组成（5 个代理）：
    ┌─────────────────────────────────────────────────────┐
    │  idea_analyst     - 想法分析师：理解并扩展用户创意   │
    │  template_picker  - 模板选择师：匹配合适的页面模板    │
    │  content_planner  - 内容规划师：规划页面各部分文案    │
    │  copywriter       - 文案撰稿人：撰写实际文字内容      │
    │  ui_ux_designer   - UI/UX 设计师：修改代码实现设计    │
    └─────────────────────────────────────────────────────┘
    
    任务流水线（7 个任务）：
    Task1: 想法分析 → Task2: 模板选择 → Task3: 内容规划
         → Task4: 文案撰写 → Task5: 首屏修改 → Task6: 特色区修改
         → Task7: 最终审核
    """

    def __init__(self, idea):
        """
        初始化落地页团队
        
        参数:
            idea (str): 用户的原始创意想法
                       例如："一个在线编程学习平台"
        
        初始化过程:
            1. 保存用户的想法
            2. 加载代理配置 (config/agents.yaml)
            3. 加载任务配置 (config/tasks.yaml)
            4. 加载模板引用表 (config/templates.json)
            5. 创建所有工具实例
            6. 初始化所有代理
            7. 设置所有任务及其依赖关系
        """
        # ==================== 第一步：保存用户输入 ====================
        self.idea = idea

        # ==================== 第二步：加载配置文件 ====================
        # 配置目录路径
        config_dir = os.path.join(os.path.dirname(__file__), "config")

        # 加载代理定义配置 (YAML 格式)
        # 包含每个代理的角色、目标、背景故事等
        with open(os.path.join(config_dir, "agents.yaml"), "r") as f:
            agents_config = yaml.safe_load(f)

        # 加载任务定义配置 (YAML 格式)
        # 包含每个任务的描述、预期输出、执行代理等
        with open(os.path.join(config_dir, "tasks.yaml"), "r") as f:
            tasks_config = yaml.safe_load(f)

        # 加载模板引用表 (JSON 格式)
        # 映射模板名称到对应的文件夹路径和描述
        with open(os.path.join(config_dir, "templates.json"), "r") as f:
            self.templates = json.load(f)

        # ==================== 第三步：创建工具实例 ====================
        # 这些工具将被挂载到各个代理上，提供具体能力
        
        # 文件操作工具：读取、写入、创建文件等
        file_tools = FileTools()
        
        # 浏览器工具：抓取和分析网页内容
        browser_tools = BrowserTools()
        
        # 搜索工具：在互联网上搜索相关信息
        search_tools = SearchTools()
        
        # 模板工具：列出可用模板、读取模板文件等
        template_tools = TemplateTools()

        # ==================== 第四步：初始化代理 ====================
        # 从 YAML 配置中创建每个代理实例
        
        # --- 代理 1：想法分析师 ---
        # 职责：深入理解用户想法，进行市场研究，扩展为一个完整的产品概念
        self.idea_analyst = Agent(
            config=agents_config["idea_analyst"],  # 从 YAML 加载角色/目标/背景
            verbose=True,
            tools=[
                search_tools.search_internet,                    # 搜索相关市场和产品信息
                browser_tools.scrape_and_summarize_website,      # 抓取参考网站分析
                file_tools.create_directory,                     # 为项目创建工作目录
                file_tools.save_to_file                          # 保存分析结果到文件
            ]
        )

        # --- 代理 2：模板选择师 ---
        # 职责：根据产品特性从 Tailwind 模板库中选择最合适的落地页模板
        self.template_picker = Agent(
            config=agents_config["template_picker"],
            verbose=True,
            tools=[
                template_tools.list_templates,                   # 列出所有可用模板
                template_tools.get_template_files_structure,     # 获取模板的文件结构
                file_tools.save_to_file                         # 保存选择结果
            ]
        )

        # --- 代理 3：内容规划师 ---
        # 职责：基于想法分析和模板结构，规划页面的整体内容架构
        self.content_planner = Agent(
            config=agents_config["content_planner"],
            verbose=True,
            tools=[
                file_tools.read_file,                            # 读取模板现有内容作为参考
                template_tools.get_template_files_structure,     # 了解模板结构
                file_tools.save_to_file                         # 保存内容规划方案
            ]
        )

        # --- 代理 4：文案撰稿人 ---
        # 职责：根据内容规划撰写实际的营销文案（标题、描述、CTA 等）
        self.copywriter = Agent(
            config=agents_config["copywriter"],
            verbose=True,
            tools=[
                file_tools.read_file,                            # 读取上下文参考
                file_tools.save_to_file                         # 保存撰写的文案
            ],
            allow_delegation=False                              # 不允许委派给其他代理
        )

        # --- 代理 5：UI/UX 设计师 ---
        # 职责：最关键的代理——直接修改 HTML/CSS 代码来实现最终设计
        self.ui_ux_designer = Agent(
            config=agents_config["ui_ux_designer"],
            verbose=True,
            tools=[
                browser_tools.scrape_and_summarize_website,      # 参考同类网站的 UI 设计
                file_tools.read_file,                            # 读取当前代码
                template_tools.get_template_files_structure,     # 理解模板结构
                file_tools.edit_file                             # 直接编辑代码文件 ⭐
            ],
            allow_delegation=False                              # 不允许委派
        )

        # ==================== 第五步：定义任务及依赖关系 ====================
        # 任务按顺序排列，后面的任务可以依赖前面任务的结果 (context)

        # === Task 1: 想法分析与扩展 ===
        # 输入：用户的原始想法
        # 输出：详细的产品概念文档（目标用户、核心功能、价值主张等）
        self.idea_analysis_task = Task(
            config=tasks_config["idea_analysis"],
            agent=self.idea_analyst,
        )

        # === Task 2: 模板选择 ===
        # 输入：Task 1 的产品概念
        # 输出：选定的模板名称和理由
        # 注意：依赖 Task 1 的输出作为 context
        self.template_selection_task = Task(
            config=tasks_config["template_selection"],
            agent=self.template_picker,
            context=[self.idea_analysis_task],                  # 依赖 Task 1
        )

        # === Task 3: 页面内容规划 ===
        # 输入：产品概念 + 选定模板的结构
        # 输出：详细的页面内容大纲（每部分写什么、用什么语气等）
        self.content_plan_task = Task(
            config=tasks_config["content_planning"],
            agent=self.content_planner,
            context=[self.template_selection_task],             # 依赖 Task 2
        )

        # === Task 4: 文案撰写 ===
        # 输入：内容规划大纲
        # 输出：实际的文案文本文件（标题、副标题、描述、CTA 等）
        self.copywriting_task = Task(
            config=tasks_config["copywriting"],
            agent=self.copywriter,
            context=[self.content_plan_task],                   # 依赖 Task 3
        )

        # === Task 5: 首屏（Hero Section）代码修改 ===
        # 这是第一个代码修改任务——修改落地页的"首屏"区域
        # 首屏是用户打开页面后看到的第一部分，至关重要
        # 输入：文案 + 原始模板代码
        # 输出：修改后的首屏 HTML/CSS
        self.hero_section_task = Task(
            config=tasks_config["hero_section_modification"],
            agent=self.ui_ux_designer,
            context=[
                self.copywriting_task,                           # 依赖 Task 4（文案）
                self.template_selection_task,                    # 依赖 Task 2（知道用哪个模板）
            ]
        )

        # === Task 6: 特征/功能区域代码修改 ===
        # 修改展示产品特色功能的区域
        # 输入：文案 + Hero 区域已完成的内容（保持一致性）
        # 输出：修改后的特征区域 HTML/CSS
        self.features_section_task = Task(
            config=tasks_config["features_section_modification"],
            agent=self.ui_ux_designer,
            context=[
                self.hero_section_task,                          # 依赖 Task 5（保持风格一致）
                self.copywriting_task,                           # 依赖 Task 4（使用正确文案）
            ]
        )

        # === Task 7: 最终审查与完善 ===
        # 最后的质量控制环节——检查整体效果并进行微调
        # 确保所有部分协调一致，没有遗漏或错误
        self.final_review_task = Task(
            config=tasks_config["final_review"],
            agent=self.ui_ux_designer,
            context=[
                self.features_section_task,                      # 依赖 Task 6
                self.copywriting_task,                           # 最终核对文案
            ]
        )

    def run(self):
        """
        执行落地页生成流程
        
        组建团队并启动所有任务。
        
        执行模式：
        - process=Process.sequential: 顺序执行模式
          任务按照定义的顺序依次执行，前一个完成后才执行下一个
          这确保了任务之间的依赖关系（context）能正确传递
        
        返回:
            None（结果直接写入了 workdir 目录中的文件）
        """
        # 创建团队实例，将所有代理和任务组装在一起
        crew = Crew(
            agents=[
                self.idea_analyst,           # 想法分析师
                self.template_picker,        # 模板选择师
                self.content_planner,         # 内容规划师
                self.copywriter,              # 文案撰稿人
                self.ui_ux_designer           # UI/UX 设计师（核心角色）
            ],

            tasks=[
                self.idea_analysis_task,           # 1. 想法分析
                self.template_selection_task,       # 2. 模板选择
                self.content_plan_task,             # 3. 内容规划
                self.copywriting_task,              # 4. 文案撰写
                self.hero_section_task,             # 5. 首屏修改
                self.features_section_task,         # 6. 特征区域修改
                self.final_review_task,             # 7. 最终审查
            ],

            process=Process.sequential,     # 顺序执行（支持 task context 传递）
            verbose=True,                   # 显示详细执行日志
            memory=True,                    # 启用记忆功能（代理可记住之前的交互）
        )

        # 启动团队，开始执行全部任务！
        result = crew.kickoff()

        print("\n\n")
        print("==========================================")
        print("Crew finished!")
        print("==========================================")

        return result
