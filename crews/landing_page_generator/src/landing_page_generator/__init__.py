"""
落地页生成器包 (Landing Page Generator Package)
================================================
CrewAI 落地页生成系统的主包。

模块结构：
├── main.py              # 程序入口（接收用户输入、执行团队、打包输出）
├── crew.py              # 核心编排（定义代理、任务、依赖关系）
├── config/              # 配置文件目录
│   ├── agents.yaml      # 5 个 AI 代理的角色/目标/背景设定
│   ├── tasks.yaml       # 7 个任务的描述和预期输出
│   └── templates.json   # 可用 Tailwind UI 模板的注册表
├── tools/               # 自定义工具目录
│   ├── browser_tools.py # 网页抓取工具
│   ├── search_tools.py  # 互联网搜索工具
│   ├── file_tools.py    # 文件读写编辑工具 ⭐ 最重要
│   └── template_tools.py# 模板查询和管理工具
└── templates/           # Tailwind 模板存放目录（需自行下载）

快速使用：
    from crew import LandingPageCrew
    
    crew = LandingPageCrew("一个在线编程学习平台")
    crew.run()
    # → 在 workdir/ 目录生成完整落地页，打包为 workdir.zip
"""
