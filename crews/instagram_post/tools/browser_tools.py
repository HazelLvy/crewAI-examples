"""
浏览器工具 (Browser Tools)
===========================
提供网页抓取和分析功能，让 AI 代理能够"阅读"和理解网页内容。

使用场景：
- 抓取产品官网，分析产品特性
- 获取竞品网站信息
- 提取页面上的营销文案和定位信息

技术实现：
- 使用 Browserless（无头浏览器云服务）渲染 JavaScript 页面
- 通过 CrewAI 的 tool 装饰器将函数包装为代理可调用的工具
"""

from crewai import Tool
from langchain.tools import tool


class BrowserTools:
    """
    浏览器工具类
    ===========
    
    提供静态方法形式的工具，供 Agent 直接调用。
    使用 @tool 装饰器将 Python 函数转换为 LangChain/CrewAI 工具。
    """

    @tool("抓取并总结网站内容")
    def scrape_and_summarize_website(website):
        """
        抓取指定网站的内容并进行智能总结
        
        这是产品分析师代理的核心工具之一，
        用于从产品官网提取关键信息。
        
        参数:
            website (str): 要抓取的网站 URL（如 https://example.com）
            
        返回:
            str: 网站内容的结构化总结，包括：
                - 公司/产品概述
                - 主要特性和功能
                - 目标用户群体
                - 营销信息和价值主张
                
        工作流程:
            1. 使用 Browserless 云服务加载网页（支持 JS 渲染）
            2. 提取页面的完整文本内容
            3. 使用 AI 模型对内容进行智能总结
            4. 返回结构化的关键信息
            
        注意:
            需要在 .env 中配置 BROWSERLESS_API_KEY
            （Browserless 是一个无头浏览器云服务，用于渲染现代 Web 应用）
        """
        # 导入 Browserless 客户端
        from langchain_community.document_loaders import AsyncChromiumLoader
        
        # 导入 HTML 内容分割器（用于处理长网页）
        from langchain_community.document_transformers import BeautifulSoupTransformer
        
        # 导入 Chain (LangChain 的处理链)
        from langchain.chains import create_extraction_chain
        from langchain_openai import ChatOpenAI

        # === 第一步：加载网页内容 ===
        # 使用 Chromium 无头浏览器加载页面
        # 这对于需要执行 JavaScript 的现代网站至关重要
        loader = AsyncChromiumLoader([website])
        docs = loader.load()

        # === 第二步：解析和转换 HTML ===
        # BeautifulSoup 将原始 HTML 转换为结构化文本
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(
            docs,
            # 只提取 body 标签内的主要内容，忽略 header/footer/navigation 等
            tags_to_extract=["body"],
            # 去除脚本、样式等无关标签
            unwanted_tags=["script", "style"],
        )

        # === 第三步：打印提取的内容（调试用途）===
        print("抓取到的网站内容:")
        print("-----------------------")
        print(docs_transformed[0].page_content[0:1000])  # 只打印前 1000 字符

        # === 第四步：返回处理后的文档 ===
        # 文档将被传递给调用此工具的 Agent 进行进一步分析
        return docs_transformed
