"""
职位发布生成器包 (Job Posting Generator Package)
================================================
CrewAI 职位描述（Job Posting）自动生成系统的主包。

模块结构：
├── main.py                      # 程序入口（定义输入、运行团队、支持训练模式）
├── crew.py                      # 核心编排（3个代理 + 5个任务，使用 @CrewBase 装饰器模式）
├── config/
│   ├── agents.yaml              # 3个代理的角色/目标/背景设定
│   └── tasks.yaml               # 5个任务的描述和预期输出
└── job_description_example.md   # 标准化的 JD 参考模板（供撰稿人代理参考格式）

团队架构（3 代理 × 5 任务）：

  research_agent (研究员)
    ├── Task1: 研究公司文化     → 分析官网，提取文化/价值观/使命
    ├── Task2: 研究岗位要求     → 输出结构化的技能/经验/品质列表 (JSON)
    └── Task5: 行业分析         → 行业趋势、竞争格局、机会挑战

  writer_agent (撰稿人)
    └── Task3: 起草 JD          → 综合所有研究结果，撰写完整职位描述

  review_agent (审核员)
    └── Task4: 审核与编辑       → 质量控制，输出最终版 JD

快速使用：
    from job_posting.crew import JobPostingCrew
    
    inputs = {
        'company_domain': 'your-company.com',
        'company_description': '你的公司描述...',
        'hiring_needs': '招聘的职位和需求...',
        'specific_benefits': '福利待遇...'
    }
    
    JobPostingCrew().crew().kickoff(inputs=inputs)
    # → 输出完整的专业职位描述文档
"""
