"""
搜索工具 (Search Tools)
========================
提供互联网搜索功能，让 AI 代理能够获取实时信息。

使用场景：
┌─────────────────────────────────────────────┐
│ 想法分析师代理                               │
│  → 搜索类似产品的落地页，分析竞品策略          │
│  → 研究目标行业的营销最佳实践                │
│  → 了解市场趋势和用户需求                    │
└─────────────────────────────────────────────┘

技术实现：
- 使用 Serper.dev（Google 搜索 API）
- 返回高质量、结构化的搜索结果

为什么用 Serper 而不是免费方案？
- Google 搜索结果质量最高（尤其英文内容）
- 支持结构化输出（标题 + 摘要 + 链接）
- 对 SEO 和营销场景的数据最全面
"""

from crewai import Tool
from langchain.tools import tool


class SearchTools:
    """
    搜索工具类
    =========
    
    提供互联网搜索能力，是想法分析师代理的主要信息来源。
    """

    @tool("互联网搜索")
    def search_internet(query):
        """
        在互联网上搜索指定关键词
        
        这是想法分析师代理的核心工具，
        用于收集市场信息和参考案例。
        
        常用查询类型：
        ──────────────────────────────────────────
        
        【产品研究】
          "SaaS landing page best practices 2024"
          → 获取 SaaS 产品落地页的设计指南
          
        【竞品分析】
          "Notion landing page design analysis"
          → 分析 Notion 的落地页策略和设计
          
        【行业趋势】
          "AI startup marketing trends"
          → 了解 AI 创业公司的最新营销趋势
          
        【文案参考】
          "best SaaS hero section copy examples"
          → 收集优秀的首屏文案范例
        
        参数:
            query (str): 搜索关键词或问题
            
        返回:
            str: 格式化的搜索结果列表
            
        底层技术:
            - 使用 Serper.dev 的 Google 搜索 API
            - 需要在 .env 中配置 SERPER_API_KEY
            - 免费额度：每月 2,500 次查询
        """
        # 导入 Serper.dev 搜索包装器
        from langchain_community.utilities import SerperAPIWrapper
        
        # 创建搜索实例（自动读取 SERPER_API_KEY）
        search = SerperAPIWrapper()
        
        # 执行搜索并返回结果
        result = search.run(query)
        return result
