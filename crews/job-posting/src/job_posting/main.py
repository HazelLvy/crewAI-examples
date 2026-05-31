"""
职位发布生成器 - 主程序入口 (Main Entry Point)
================================================
本程序使用 CrewAI 框架自动生成专业的职位描述（Job Posting）。

功能：
  输入公司信息和招聘需求 → AI 团队协作 → 输出完整的职位描述文档

运行方式：
  python main.py                    # 直接运行（使用默认示例数据）
  python main.py train <迭代次数>    # 训练模式（让团队从反馈中学习）

输出：
  一份完整、专业的招聘职位描述文档

使用场景：
  - HR 快速生成标准化的 JD（职位描述）
  - 确保职位描述涵盖所有必要信息
  - 根据公司品牌调性定制文案风格
"""

import sys
from job_posting.crew import JobPostingCrew


def run():
    """
    运行职位描述生成团队
    
    工作流程：
    1. 定义输入参数（公司域名、公司简介、招聘需求、福利待遇）
    2. 创建 JobPostingCrew 实例并启动执行
    3. 自动将输入参数注入到代理和任务中
    
    输入参数说明 (inputs):
    ┌────────────────────┬──────────────────────────────────────────┐
    │ company_domain     │ 公司官网或招聘页面 URL                     │
    │                    │ 用于抓取公司信息以了解品牌风格              │
    ├────────────────────┼──────────────────────────────────────────┤
    │ company_description│ 公司/组织的详细描述                        │
    │                    │ 用于生成符合企业文化的职位介绍部分          │
    ├────────────────────┼──────────────────────────────────────────┤
    │ hiring_needs       │ 具体的招聘需求                            │
    │                    │ 包含职位名称、地点、时间等关键信息           │
    ├────────────────────┼──────────────────────────────────────────┤
    │ specific_benefits │ 该职位的特定福利待遇                       │
    │                    │ 将被纳入职位描述的福利部分                 │
    └────────────────────┴──────────────────────────────────────────┘
    
    注意事项：
    - 请将示例中的占位符数据替换为你自己的实际信息
    - 公司域名用于抓取参考信息，确保可访问性
    - hiring_needs 越详细，生成的 JD 越准确
    """
    # 定义输入参数 — 替换为你的实际数据即可
    inputs = {
        'company_domain': 'careers.wbd.com',   # 公司域名（用于抓取公司信息）
        # 公司描述 — 用于了解企业文化，生成匹配的职位介绍
        'company_description': "Warner Bros. Discovery is a premier global media and entertainment company, offering audiences the world's most differentiated and complete portfolio of content, brands and franchises across television, film, sports, news, streaming and gaming. We're home to the world's best storytellers, creating world-class products for consumers",
        # 招聘需求 — 职位名称、工作地点、时间等关键信息
        'hiring_needs': 'Production Assistant, for a TV production set in Los Angeles in June 2025',
        # 该职位特有的福利待遇
        'specific_benefits': 'Weekly Pay, Employee Meals, healthcare',
    }
    
    # 创建团队实例并启动执行
    # kickoff() 方法触发全部任务开始运行
    JobPostingCrew().crew().kickoff(inputs=inputs)


def train():
    """
    训练模式 - 让团队从反馈中学习
    
    什么是训练（Training）？
    ------------------------
    CrewAI 的训练功能允许你对团队的输出进行评分，
    然后系统会根据评分调整代理的行为，使后续输出更接近预期。
    
    使用场景：
    - 首次运行后对结果不满意
    - 希望团队学会某种特定的写作风格
    - 需要反复迭代优化输出质量
    
    参数:
        n_iterations: 训练迭代次数（通过命令行传入）
                      例如: python main.py train 10 表示训练10轮
        
    工作流程:
    1. 执行任务并获取初始输出
    2. 人工/自动对输出进行评分和反馈
    3. 根据反馈调整代理参数
    4. 重复步骤1-3直到达到指定迭代次数
    """
    inputs = {
        'company_domain': 'careers.wbd.com',
        'company_description': "Warner Bros. Discovery is a premier global media and entertainment company, offering audiences the world's most differentiated and complete portfolio of content, brands and franchises across television, film, sports, news, streaming and gaming. We're home to the world's best storytellers, creating world-class products for consumers",
        'hiring_needs': 'Production Assistant, for a TV production set in Los Angeles in June 2025',
        'specific_benefits': 'Weekly Pay, Employee Meals, healthcare',
    }
    try:
        # 调用 crew.train() 方法而非 kickoff()
        # sys.argv[1] 是命令行传入的训练轮数
        JobPostingCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
