"""
落地页生成器 - 主程序入口
==========================
本程序是 Landing Page Generator 的入口点。

工作流程：
  用户输入想法 → 创建团队并执行 → 打包生成 ZIP 文件

输出：
  workdir.zip - 包含完整的落地页 HTML/CSS/JS 文件
"""

import os
import shutil
# dedent: 用于格式化多行字符串（去除缩进）
from textwrap import dedent

# 导入落地页团队类
from crew import LandingPageCrew


if __name__ == "__main__":
    # ==================== 欢迎信息与警告 ====================
    print("Welcome to Idea Generator")
    print(dedent("""
    ! YOU MUST FORK THIS BEFORE USING IT !
    """))

    # 费用和时间提醒
    # 默认使用 GPT-4，每次运行费用约 $2-9，耗时约 10-45 分钟
    print(dedent("""
        Disclaimer: This will use gpt-4 unless you changed it 
        not to, and by doing so it will cost you money (~2-9 USD).
        The full run might take around ~10-45m. Enjoy your time back.\n\n
      """
    ))

    # ==================== 获取用户输入 ====================
    # 用户输入：描述你的产品/项目想法
    # 例如："一个在线编程学习平台" 或 "AI 驱动的健康饮食 App"
    idea = input("# Describe what is your idea:\n\n")

    # ==================== 环境检查 ====================
    
    # 检查/创建工作目录（用于存放生成的文件）
    if not os.path.exists("./workdir"):
        os.mkdir("./workdir")

    # 检查模板目录是否包含 Tailwind UI 模板
    # Tailwind 模板是生成落地页的基础骨架，必须提前放入 templates/ 目录
    if len(os.listdir("./templates")) == 0:
        print(
            dedent("""
            !!! NO TEMPLATES FOUND !!!
            ! YOU MUST FORK THIS BEFORE USING IT !
            
            Templates are not included as they are Tailwind templates. 
            Place Tailwind individual template folders in `./templates`, 
            if you have a license you can download them at
            https://tailwindui.com/templates, their references are at
            `config/templates.json`.
            
            This was not tested this with other templates, 
            prompts in `tasks.py` might require some changes 
            for that to work.
            
            !!! STOPPING EXECUTION !!!
            """)
        )
        exit()  # 无模板则退出

    # ==================== 执行团队任务 ====================
    
    # 创建落地页团队实例，传入用户的想法
    crew = LandingPageCrew(idea)
    
    # 运行团队：代理们将协同完成落地页的规划、选择和定制
    crew.run()

    # ==================== 打包结果 ====================
    
    # 将生成的所有文件打包为 ZIP 格式，方便下载
    zip_file = "workdir"
    shutil.make_archive(zip_file, 'zip', 'workdir')  # 生成 workdir.zip
    
    # 清理临时工作目录（已打包完毕，不再需要原文件）
    shutil.rmtree('workdir')

    # 输出完成提示
    print("\n\n")
    print("==========================================")
    print("DONE!")
    print(f"You can download the project at ./{zip_file}.zip")
    print("==========================================")
