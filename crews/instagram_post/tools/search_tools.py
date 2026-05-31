"""
搜索工具 (Search Tools)
========================
提供互联网搜索功能，让 AI 代理能够获取实时信息。

使用场景：
- 搜索竞品信息和市场动态
- 查找行业趋势和最新新闻
- 补充产品分析所需的外部数据
- 研究 Instagram 营销最佳实践

技术实现：
- 使用 Serper（Google 搜索 API）获取高质量搜索结果
- 通过 @tool 装饰器包装为 CrewAI 工具

为什么用 Serper 而不是 DuckDuckGo？
- Serper 返回 Google 搜索结果，质量和相关性更高
- 支持结构化的结果格式（标题、摘要、链接）
- 对中文搜索的支持更好（通过 Google）
"""

from crewai import Tool
from langchain.tools import tool


class SearchTools:
    """
    搜索工具类
    =========
    
    提供互联网搜索能力，是代理获取外部信息的主要手段。
    """

    @tool("互联网搜索")
    def search_internet(query):
        """
        在互联网上搜索指定关键词
        
        这是使用最频繁的工具之一，支持多种查询类型：
        - 事实查询："Python crewAI framework"
        - 竞品分析："Nike vs Adidas Instagram marketing"
        - 行业趋势："social media marketing trends 2024"
        - 技术文档："Instagram API best practices"
        
        参数:
            query (str): 搜索关键词或问题
            
        返回:
            str: 格式化的搜索结果列表，每条包含：
                - 标题 (title)
                - 内容摘要 (snippet)
                - 来源链接 (link)
                
        使用示例（Agent 自动调用）:
            >>> SearchTools.search_internet("Apple iPhone 15 marketing strategy")
            # 返回 Apple iPhone 15 相关的营销策略文章和信息
            
        底层技术:
            - 使用 Serper.dev 的 Google 搜索 API
            - 需要在 .env 中配置 SERPER_API_KEY
            - 免费额度：每月 2,500 次查询
        """
        # 导入 Serper.dev 的 Google 搜索工具
        from langchain_community.utilities import SerperAPIWrapper
        
        # 创建 Serper 搜索实例
        # 会自动从环境变量读取 SERPER_API_KEY
        search = SerperAPIWrapper()
        
        # 执行搜索并返回结果
        result = search.run(query)
        
        return result
