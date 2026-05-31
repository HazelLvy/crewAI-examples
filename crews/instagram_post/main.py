"""
Instagram 帖子生成系统 - 主程序
=================================
本程序使用 CrewAI 框架，通过多代理协作自动完成 Instagram 营销帖子的创作。

工作流程：
第一阶段（文案团队 Copy Crew）：
  产品分析 → 竞品分析 → 营销策划 → 文案撰写

第二阶段（图片团队 Image Crew）：
  图片拍摄描述 → 创意总监审核

输出结果：
  - ad_copy: Instagram 帖子的文案内容
  - image: 用于 Midjourney 等 AI 绘图工具的提示词
"""

# 加载 .env 文件中的环境变量（API Key 等）
from dotenv import load_dotenv
load_dotenv()

from textwrap import dedent
from crewai import Agent, Crew

# 导入自定义的任务类和代理类
from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents


# ==================== 全局初始化 ====================
# 创建任务工厂和代理工厂实例（单例模式，全局共享）
tasks = MarketingAnalysisTasks()
agents = MarketingAnalysisAgents()


# ==================== 用户输入 ====================
print("## Welcome to the marketing Crew")
print('-------------------------------')

# 用户输入：要推广的产品网站 URL
product_website = input("What is the product website you want a marketing strategy for?\n")

# 用户输入：产品的额外信息或对帖子的特殊要求
product_details = input("Any extra details about the product and or the instagram post you want?\n")


# ==================== 第一阶段：文案团队 (Copy Crew) ====================
# 团队职责：分析产品和竞品，制定营销策略，撰写 Instagram 帖子文案

# --- 创建文案团队的 3 个代理 ---
# 1. 产品竞品分析师：负责研究产品特性和市场竞争情况
product_competitor_agent = agents.product_competitor_agent()
# 2. 策略规划师：负责制定整体营销策略和活动方案
strategy_planner_agent = agents.strategy_planner_agent()
# 3. 创意文案撰稿人：负责撰写吸引人的 Instagram 广告文案
creative_agent = agents.creative_content_creator_agent()

# --- 创建文案团队的 4 个任务 ---
# 任务1：产品网站分析 - 深入了解产品特性、目标用户、价值主张
website_analysis = tasks.product_analysis(product_competitor_agent, product_website, product_details)
# 任务2：竞品分析 - 分析竞争对手的营销策略和市场定位
market_analysis = tasks.competitor_analysis(product_competitor_agent, product_website, product_details)
# 任务3：营销活动策划 - 基于前两步分析结果制定营销策略
campaign_development = tasks.campaign_development(strategy_planner_agent, product_website, product_details)
# 任务4：Instagram 文案撰写 - 创作最终的广告文案
write_copy = tasks.instagram_ad_copy(creative_agent)

# --- 组建文案团队并执行 ---
copy_crew = Crew(
    agents=[
        product_competitor_agent,     # 产品分析师
        strategy_planner_agent,       # 策略规划师
        creative_agent                # 创意文案
    ],
    tasks=[
        website_analysis,             # 产品分析
        market_analysis,              # 竞品分析
        campaign_development,         # 营销策划
        write_copy                    # 文案撰写
    ],
    verbose=True                       # 显示详细执行日志
)

# 启动文案团队，获取最终文案
ad_copy = copy_crew.kickoff()


# ==================== 第二阶段：图片团队 (Image Crew) ====================
# 团队职责：根据文案生成 AI 图片的描述提示词（用于 Midjourney / DALL-E 等）

# --- 创建图片团队的 2 个代理 ---
# 1. 高级摄影师：负责构思视觉画面并生成摄影描述
senior_photographer = agents.senior_photographer_agent()
# 2. 首席创意总监：负责审核和优化图片创意描述
chief_creative_diretor = agents.chief_creative_diretor_agent()

# --- 创建图片团队的 2 个任务 ---
# 任务1：拍照/构图 - 根据文案内容生成详细的画面描述（Midjourney 提示词）
take_photo = tasks.take_photograph_task(senior_photographer, ad_copy, product_website, product_details)
# 任务2：审核照片 - 创意总监对画面描述进行质量把控和优化
approve_photo = tasks.review_photo(chief_creative_diretor, product_website, product_details)

# --- 组建图片团队并执行 ---
image_crew = Crew(
    agents=[
        senior_photographer,           # 高级摄影师
        chief_creative_diretor         # 首席创意总监
    ],
    tasks=[
        take_photo,                    # 构思画面
        approve_photo                  # 审核优化
    ],
    verbose=True
)

# 启动图片团队，获取图片描述（用于 AI 绘图工具）
image = image_crew.kickoff()


# ==================== 输出最终结果 ====================
print("\n\n########################")
print("## Here is the result")
print("########################\n")

# 输出1：Instagram 帖子文案（可直接发布到 Instagram）
print("Your post copy:")
print(ad_copy)

# 输出2：AI 绘图提示词（可复制到 Midjourney / DALL-E / Stable Diffusion 使用）
print("'\n\nYour midjourney description:")
print(image)
