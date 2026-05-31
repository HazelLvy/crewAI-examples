"""
自定义工具包 (Tools Package)
==============================
本包包含 Instagram 营销系统中代理使用的所有自定义工具。

工具列表：
- browser_tools.py : 网页抓取和内容分析工具
- search_tools.py  : 互联网搜索工具
- calculator_tools.py: 数学计算工具
- sec_tools.py     : SEC（美国证券交易委员会）财务数据查询工具

使用方式：
在 agents.py 中通过 import 导入，然后挂载到 Agent 的 tools 参数上：
    from tools.browser_tools import BrowserTools
    
    Agent(
        ...,
        tools=[BrowserTools.scrape_and_summarize_website],
    )
"""
