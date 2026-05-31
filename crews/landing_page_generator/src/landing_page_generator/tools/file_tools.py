"""
文件操作工具 (File Tools)
==========================
提供文件系统的读写和编辑功能，是落地页生成系统中最关键的工具集。

⭐ 为什么这个工具最重要？
因为 UI/UX 设计师代理需要通过此工具直接修改 HTML/CSS 代码文件！
其他代理也需要用此工具保存分析结果、文案等中间产出。

使用场景：
┌──────────────────┬─────────────────────────────┬──────────────┐
│ 工具方法          │ 使用代理                    │ 用途          │
├──────────────────┼─────────────────────────────┼──────────────┤
│ create_directory │ 想法分析师                   │ 创建项目目录  │
│ save_to_file     │ 想法分析师/模板选择师/       │ 保存分析结果  │
│                 │ 内容规划师/文案撰稿人         │ 和文案文档    │
│ read_file        │ 内容规划师/UI设计师          │ 读取模板代码  │
│ edit_file        │ UI/UX 设计师 ⭐              │ 直接修改代码! │
└──────────────────┴─────────────────────────────┴──────────────┘

工作目录说明：
所有操作都在 ./workdir/ 目录下进行：
  workdir/
    ├── product-concept.md       ← 想法分析结果
    ├── template-selection.md    ← 模板选择结果
    ├── content-plan.md          ← 内容规划方案
    ├── copywriting.md           ← 文案内容
    └── <template_files>/        ← 实际的 HTML/CSS 文件（从模板复制过来）
"""

from crewai import Tool
from langchain.tools import tool
import os


class FileTools:
    """
    文件操作工具类
    =============
    
    提供 4 个核心方法，覆盖文件操作的完整生命周期：
    创建目录 → 写入文件 → 读取文件 → 编辑文件
    """

    @tool("创建目录")
    def create_directory(directory_path):
        """
        创建新的目录（文件夹）
        
        使用时机：
        - 想法分析师在开始分析前，为当前项目创建工作目录
        - 确保后续所有输出文件有统一的存放位置
        
        参数:
            directory_path (str): 要创建的目录路径
                                 例如："./workdir/my-project"
            
        返回:
            str: 创建成功的信息
            
        示例调用（由 Agent 自动触发）:
            >>> FileTools.create_directory("./workdir")
            # 在当前目录下创建 workdir 文件夹
        """
        os.makedirs(directory_path, exist_ok=True)   # exist_ok: 目录已存在时不报错
        return f"Directory '{directory_path}' created successfully."

    @tool("保存内容到文件")
    def save_to_file(file_path, content):
        """
        将文本内容写入（保存到）指定文件
        
        这是最常用的工具之一——几乎所有代理都会用它来保存产出。
        
        典型用途：
        - 想法分析师 → 保存产品概念文档 (product-concept.md)
        - 模板选择师 → 保存选择报告 (template-selection.md)
        - 内容规划师 → 保存内容规划 (content-plan.md)
        - 文案撰稿人 → 保存最终文案 (copywriting.md)
        
        参数:
            file_path (str): 目标文件路径
                             例如："./workdir/product-concept.md"
            content (str):   要写入的文本内容
                             例如：完整的 Markdown 格式产品分析报告
            
        返回:
            str: 保存成功的确认信息
            
        注意事项:
            - 如果父目录不存在会自动创建
            - 如果文件已存在会被覆盖（覆盖写入模式）
        """
        # 确保文件的父目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 写入文件（UTF-8 编码）
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"Content saved to '{file_path}' successfully."

    @tool("读取文件内容")
    def read_file(file_path):
        """
        读取并返回指定文件的完整内容
        
        使用时机：
        - 内容规划师：读取选定模板的 HTML/CSS，了解其结构后再做规划
        - 文案撰稿人：阅读 product-concept.md 和 content-plan.md 作为参考
        - UI/UX 设计师：读取当前的 HTML 文件，了解现有代码再进行修改
        
        参数:
            file_path (str): 要读取的文件路径
                             例如："./templates/saas-template/index.html"
                              或 "./workdir/product-concept.md"
            
        返回:
            str: 文件的完整文本内容
            
        支持的文件类型:
            - .html / .htm（网页源码）
            - .css（样式表）
            - .md / .txt（文本文档）
            - .js（JavaScript 代码）
            - 基本上任何纯文本文件
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content

    @tool("编辑文件内容")  # ⭐ 最关键的工具！
    def edit_file(file_path, old_content, new_content):
        """
        编辑文件中的指定内容 —— 替换旧内容为新内容
        
        ⭐⭐⭐ 这是整个项目中最重要的工具！！！
        
        UI/UX 设计师代理通过此工具直接修改落地页的 HTML/CSS 代码。
        它是连接 "AI 规划" 和 "实际产出" 的桥梁。
        
        工作原理：
        1. Agent 先用 read_file() 读取当前文件内容
        2. Agent 分析代码，决定要修改哪一部分
        3. Agent 调用 edit_file()，指定要替换的旧内容和新的替换内容
        4. 文件被更新，完成一次代码修改
        
        典型修改场景：
        ──────────────────────────────────────────
        
        【修改主标题】
          old_content: "<h1>Welcome to Our App</h1>"
          new_content: "<h1>AI 驱动的编程学习平台</h1>"
          
        【修改 CTA 按钮】
          old_content: "<button>Get Started</button>"
          new_content: "<button>立即免费开始学习</button>"
          
        【更新描述文字】
          old_content: "<p>A simple app for everyone</p>"
          new_content: "<p>通过 AI 个性化推荐，让每个人都能找到适合自己的学习路径...</p>"
          
        【替换颜色变量】（CSS 中）
          old_content: "--primary-color: #3b82f6;"
          new_content: "--primary-color: #6366f1;"
        
        参数:
            file_path (str):    要编辑的文件路径
            old_content (str):  要被替换的原始内容（必须精确匹配）
            new_content (str):  新的替换内容
            
        返回:
            str: 编辑成功/失败的确认信息
            
        重要提示:
            - old_content 必须与文件中的内容完全一致（包括空格和换行）
            - 如果找不到匹配的内容，编辑会失败并返回错误信息
            - 建议每次只替换一小段内容，避免大范围替换导致意外错误
        """
        try:
            # 读取文件全部内容
            with open(file_path, "r", encoding="utf-8") as f:
                current_content = f.read()

            # 执行字符串替换
            if old_content in current_content:
                new_file_content = current_content.replace(old_content, new_content)

                # 将更新后的内容写回文件
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_file_content)

                return f"File '{file_path}' edited successfully. Replaced specified content."
            else:
                return (
                    f"Error: The specified old_content was not found in '{file_path}'. "
                    f"Please check that the content matches exactly."
                )
                
        except Exception as e:
            return f"Error editing file '{file_path}': {str(e)}"
