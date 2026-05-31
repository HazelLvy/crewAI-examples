"""
模板工具 (Template Tools)
==========================
提供 Tailwind CSS 模板的管理和查询功能。

使用场景：
┌─────────────────────────────────────────────┐
│ 模板选择师代理                               │
│  → 列出所有可用的模板选项                    │
│  → 查看每个模板的文件结构                    │
│  → 基于产品特性选择最合适的模板              │
│                                              │
│ 内容规划师代理                               │
│  → 了解选定模板的页面结构                    │
│  → 根据实际 HTML 结构来规划内容              │
│                                              │
│ UI/UX 设计师代理                             │
│  → 理解模板的文件组织方式                    │
│  → 找到需要修改的具体文件                    │
└─────────────────────────────────────────────┘

关于模板：
---------
本项目使用 Tailwind UI（https://tailwindui.com）的模板作为落地页的基础骨架。
Tailwind UI 是由 Tailwind CSS 官方提供的高质量商业模板库。

模板文件结构示例：
  templates/
    └── saas-landing-page/
        ├── index.html          ← 主页面文件（主要修改目标）
        ├── css/
        │   └── style.css       ← 样式文件
        ├── js/
        │   └── main.js         ← JavaScript 文件
        └── assets/
            └── images/         ← 图片资源

注意：模板文件夹需单独下载并放入 ./templates 目录（未包含在仓库中）
"""

import os
import json

from crewai import Tool
from langchain.tools import tool


class TemplateTools:
    """
    模板工具类
    =========
    
    提供模板查询和管理能力，帮助代理选择和了解可用的模板。
    """

    @tool("列出可用模板")
    def list_templates():
        """
        列出所有可用的 Tailwind UI 模板
        
        从 config/templates.json 中读取已注册的模板列表，
        为模板选择师提供完整的可选方案。
        
        返回:
            str: 所有可用模板的名称、描述和适用场景
            
        输出示例:
            "可用模板列表：
            1. SaaS Landing Page - Light Mode
               适合：软件/SaaS 产品，干净专业风格
            2. Portfolio Landing Page - Creative
               适合：设计作品展示，创意风格
            ..."
            
        使用流程:
            1. 模板选择师调用此方法获取所有选项
            2. 根据产品概念分析结果进行匹配筛选
            3. 选定最合适的模板后继续下一步任务
        """
        # 配置文件路径：templates.json 存储了所有模板的元数据
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "templates.json")
        
        # 读取 JSON 格式的模板注册表
        with open(config_path, "r") as f:
            templates = json.load(f)
        
        # 格式化输出模板信息
        result = "可用模板列表：\n\n"
        for idx, (name, info) in enumerate(templates.items(), start=1):
            result += f"{idx}. {name}\n"
            result += f"   描述: {info['description']}\n"
            result += f"   可编辑区域: {', '.join(info['sections'])}\n\n"
        
        return result

    @tool("获取模板文件结构")
    def get_template_files_structure(template_name=None):
        """
        获取指定模板（或所有模板）的文件目录结构
        
        这个工具帮助代理理解模板的组织方式，
        从而知道应该编辑哪些文件来实现设计需求。
        
        参数:
            template_name (str): 可选，指定要查看的模板名称
                                如果不传则返回第一个找到的模板的结构
            
        返回:
            str: 模板的完整目录结构和文件列表
            
        典型输出:
            "模板 'SaaS Landing Page' 的文件结构：
            
            📁 saas-landing-page/
            ├── 📄 index.html          (主页面 - 主要修改目标!)
            ├── 📁 css/
            │   └── 📄 style.css      (样式表)
            ├── 📁 js/
            │   └── 📄 main.js        (交互脚本)
            └── 📁 assets/
                └── 📁 images/        (图片资源)"
                
        为什么需要此工具？
        ──────────────────
        1. **内容规划师**需要知道模板有哪些区域可以填写内容
        2. **UI/UX 设计师**需要知道具体哪个 .html 文件是主页面
        3. 不同模板的文件组织可能不同，不能假设固定结构
        """
        # 模板根目录
        templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        
        if template_name:
            # 如果指定了模板名，直接查找该模板
            template_path = os.path.join(templates_dir, template_name)
            if os.path.exists(template_path):
                return self._get_directory_structure(template_path, template_name)
            else:
                return f"Error: Template '{template_name}' not found."
        else:
            # 未指定模板名 → 自动查找 templates 目录下第一个子文件夹
            if os.path.exists(templates_dir):
                subdirs = [d for d in os.listdir(templates_dir) 
                          if os.path.isdir(os.path.join(templates_dir, d))]
                if subdirs:
                    # 取第一个模板目录
                    first_template = os.path.join(templates_dir, subdirs[0])
                    return self._get_directory_structure(first_template, subdirs[0])
                else:
                    return "Error: No templates found in the templates directory."
            else:
                return "Error: Templates directory does not exist."

    def _get_directory_structure(self, root_dir, dir_name):
        """
        内部方法：递归生成目录结构的字符串表示
        
        参数:
            root_dir: 要扫描的根目录路径
            dir_name: 显示用的目录名称
            
        返回:
            str: 格式化的目录树形结构
        """
        result = f"📁 {dir_name}/\n"
        
        for root, dirs, files in os.walk(root_dir):
            # 计算当前层级缩进
            level = root.replace(root_dir, '').count(os.sep)
            indent = "    " * (level + 1)  # 缩进空格
            
            # 排除 __pycache__ 和隐藏目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            # 显示子目录
            for dirname in dirs:
                result += f"{indent}📁 {dirname}/\n"
            
            # 显示文件
            for filename in files:
                # 根据扩展名添加图标
                icon = "📄"  # 默认文件图标
                ext = os.path.splitext(filename)[1].lower()
                if ext in ['.html', '.htm']:
                    icon = "🌐"   # HTML 文件
                elif ext == '.css':
                    icon = "🎨"   # CSS 文件
                elif ext == '.js':
                    icon = "⚙️"   # JS 文件
                elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
                    icon = "🖼️"   # 图片文件
                    
                result += f"{indent}{icon} {filename}\n"
        
        return result
