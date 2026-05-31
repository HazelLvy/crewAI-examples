"""
落地页生成器 - 工具包 (Tools Package)
========================================
本包包含落地页生成系统中代理使用的所有自定义工具。

工具列表：
├── browser_tools.py    - 网页抓取和分析工具
├── search_tools.py     - 互联网搜索工具
├── file_tools.py       - 文件操作工具（读取、写入、编辑、创建目录）
└── template_tools.py   - 模板相关工具（列出模板、获取结构）

使用方式：
在 crew.py 中导入后挂载到 Agent 的 tools 参数上：
    from tools.file_tools import FileTools
    from tools.search_tools import SearchTools
    
    Agent(
        ...,
        tools=[
            FileTools.read_file,
            FileTools.save_to_file,
            SearchTools.search_internet,
        ]
    )
"""
