"""
浏览器工具 (Browser Tools)
===========================
提供网页抓取和内容分析功能，让 AI 代理能够"阅读"和理解网页内容。

使用场景：
┌─────────────────────────────────────────────┐
│ 想法分析师代理                               │
│  → 抓取竞品网站，学习他们的落地页设计         │
│  → 分析同类产品的文案风格和结构              │
│                                              │
│ UI/UX 设计师代理                             │
│  → 参考优秀网站的 UI 设计模式                │
│  → 获取设计灵感用于代码修改                  │
└─────────────────────────────────────────────┘

技术实现：
- 使用 Browserless（无头浏览器云服务）渲染 JavaScript 页面
- 通过 BeautifulSoup 解析和清理 HTML
- 通过 @tool 装饰器包装为 CrewAI 可调用的工具
"""

from crewai import Tool
from langchain.tools import tool


class BrowserTools:
    """
    浏览器工具类
    ===========
    
    提供静态方法形式的工具，供 Agent 直接调用。
    """

    @tool("抓取并总结网站内容")
    def scrape_and_summarize_website(website):
        """
        抓取指定网站的内容并进行智能总结
        
        这是想法分析师和 UI/UX 设计师的关键工具之一，
        用于从参考网站提取关键信息或获取设计灵感。
        
        参数:
            website (str): 要抓取的网站 URL
                          例如："https://www.linear.app"
                          或 "https://stripe.com"
            
        返回:
            str: 网站内容的结构化总结文本
            
        工作流程:
            1. 使用 AsyncChromium（异步 Chromium 无头浏览器）加载页面
               → 这对现代 JavaScript 渲染的单页应用 (SPA) 至关重要
            2. BeautifulSoup 将 HTML 转换为可读文本
               → 去除 script、style、nav、footer 等无关标签
               → 只保留 body 中主要内容
            3. 返回清理后的文档，由 Agent 进一步分析和总结
            
        注意事项:
            - 需要在 .env 中配置 BROWSERLESS_API_KEY
            - Browserless 是付费服务（有免费额度）
            - 对于纯静态 HTML 页面可考虑用更轻量的方案
        """
        # 导入 LangChain 的异步 Chromium 加载器
        # 用于渲染需要 JavaScript 执行的现代网页
        from langchain_community.document_loaders import AsyncChromiumLoader
        
        # 导入 HTML 转换器
        # BeautifulSoup 用于将原始 HTML 转换为干净的文本
        from langchain_community.document_transformers import BeautifulSoupTransformer
        
        # === 第一步：使用无头浏览器加载网页 ===
        # AsyncChromium 可以执行 JavaScript，
        # 这对于 React/Vue/Angular 等现代前端框架构建的页面是必需的
        loader = AsyncChromiumLoader([website])
        docs = loader.load()

        # === 第二步：解析和转换 HTML ===
        # 提取 body 内容，去除 script/style/nav/footer 等无关元素
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(
            docs,
            tags_to_extract=["body"],     # 只提取 <body> 标签内的内容
            unwanted_tags=["script", "style", "nav", "footer", "header"],
                                        # 排除这些不需要的标签
        )

        # === 第三步：返回处理后的结果 ===
        print("抓取到的网站内容:")
        print("-----------------------")
        # 打印前 1000 字符用于调试确认
        print(docs_transformed[0].page_content[0:1000])

        return docs_transformed
