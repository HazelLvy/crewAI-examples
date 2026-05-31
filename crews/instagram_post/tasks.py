"""
Instagram 营销任务定义 (Tasks)
================================
本文件定义了 Instagram 帖子生成系统中的 6 个任务。

任务流程（两阶段流水线）：

阶段一：文案团队 (Copy Crew) - 4 个任务
  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐     ┌──────────────┐
  │ product_     │ →   │ competitor_  │ →   │ campaign_      │ →   │ instagram_   │
  │ analysis     │     │ analysis     │     │ development    │     │ ad_copy      │
  │ 产品分析      │     │ 竞品分析      │     │ 营销策划        │     │ 文案撰写      │
  └──────────────┘     └──────────────┘     └────────────────┘     └──────────────┘

阶段二：图片团队 (Image Crew) - 2 个任务
  ┌───────────────────┐     ┌──────────────────┐
  │ take_photograph_  │ →   │ review_photo      │
  │ task              │     │                   │
  │ 构思画面描述       │     │ 创意总监审核       │
  └───────────────────┘     └──────────────────┘
"""

from crewai import Task


class MarketingAnalysisTasks:
    """
    营销分析任务工厂类
    ==================
    
    创建 6 个任务，分为两组：
    - Copy Crew 任务（4个）：产品分析 → 竞品分析 → 策划 → 文案
    - Image Crew 任务（2个）：拍照描述 → 审核优化
    
    每个任务都绑定到特定的代理，并接收必要的上下文参数。
    """

    # ================================================================
    #                 文案团队任务 (Copy Crew Tasks)
    # ================================================================

    def product_analysis(self, agent, product_website, product_details):
        """
        任务1：产品网站分析
        
        目的：深入了解要推广的产品
        
        执行代理：product_competitor_agent（产品/竞品分析师）
        
        参数:
            agent:           执行此任务的代理实例
            product_website: 用户输入的产品官网 URL
            product_details: 用户提供的额外产品信息
            
        输出内容：
            - 产品核心特性和功能
            - 目标用户画像
            - 品牌价值主张
            - 当前市场定位
            - 产品独特卖点（USP）
        """
        return Task(
            description="""对给定的 {product_website} URL 进行全面的产品分析，
                并考虑任何额外的 {product_details}。
                你的分析应涵盖：
                
                1. **产品特性与功能**：详细说明产品提供什么
                2. **目标受众**：识别理想客户的人口统计、兴趣和痛点
                3. **品牌定位**：了解品牌在市场中的定位方式
                4. **独特卖点**：识别使该产品与众不同的因素
                5. **当前营销信息**：评估网站上现有的营销文案和策略
                
                使用提供的工具收集尽可能多的相关信息。
                务必彻底且数据驱动地进行分析。""".format(
                    product_website=product_website,
                    product_details=product_details
                ),

            expected_output="""一份全面的产品分析报告，
                详细说明关键产品特性、目标受众洞察、
                品牌定位以及从 {product_website} 收集的独特卖点。""".format(
                    product_website=product_website
                ),
            agent=agent,
        )

    def competitor_analysis(self, agent, product_website, product_details):
        """
        任务2：竞争对手分析
        
        目的：研究市场竞争格局，找出差异化机会
        
        执行代理：product_competitor_agent（产品/竞品分析师）
        
        参数:
            agent:           执行此任务的代理
            product_website: 产品网站 URL（用于推断行业和竞品）
            product_details: 额外产品信息
            
        输出内容：
            - 主要竞争对手列表
            - 各竞品的优势与劣势
            - 竞品的 Instagram 营销策略
            - 市场空白和机会点
        """
        return Task(
            description="""使用先前产品分析的见解，对主要竞争对手进行全面的研究。
                基于 {product_website} 和 {product_details} 中提供的信息：
                
                1. **识别直接竞争对手**：寻找销售类似产品或服务的公司
                2. **分析其营销策略**：特别关注他们的 Instagram 表现
                3. **评估优势与劣势**：他们做得好的地方？哪里有改进空间？
                4. **确定市场空白**：寻找竞争对手未充分利用的机会
                5. **收集创意灵感**：注意成功的活动和可以改进的策略
                
                使用搜索工具查找有关竞争对手的最新信息。""".format(
                    product_website=product_website,
                    product_details=product_details
                ),

            expected_output="""一份详细的竞争分析报告，
                包括主要竞争对手及其营销策略的列表、
                对其优势和劣势的分析，以及
                可以为我们的 Instagram 营销策略利用的关键机会。""",
            agent=agent,
        )

    def campaign_development(self, agent, product_website, product_details):
        """
        任务3：Instagram 营销活动策划
        
        目的：基于前两步分析结果，制定完整的 Instagram 营销策略
        
        执行代理：strategy_planner_agent（策略规划师）
        
        参数:
            agent:           执行此任务的代理（策略规划师）
            product_website: 产品网站 URL
            product_details: 额外产品信息
            
        输出内容：
            - 整体营销主题和方向
            - 目标受众细分策略
            - 内容类型建议（图片/视频/轮播等）
            - 发布时间建议
            - 标签 (hashtags) 策略
            - 关键绩效指标 (KPIs)
            
        注意：
            此任务会自动接收到 task_1 和 task_2 的输出作为 context
            （CrewAI 的任务链机制）
        """
        return Task(
            description="""利用产品分析和竞争研究的见解，为 {product_website}
                制定全面的 Instagram 营销活动策略，考虑 {product_details}。
                
                你应制定一个详细的计划，包括：
                
                1. **活动目标**：明确、可衡量的目标
                2. **目标受众策略**：如何有效地触达理想的客户
                3. **内容策略**：
                   - 内容支柱和主题
                   - 建议的内容格式（例如：照片、视频、Reels、轮播图）
                   - 视觉风格指南建议
                4. **标签策略**：相关的和热门的标签以最大化覆盖面
                5. **发布日历**：最佳发布时间和频率的建议
                6. **参与度策略**：如何鼓励互动和建立社区
                7. **成功指标**：用于追踪活动的 KPIs
                
                确保策略具有创意、可执行性，并与品牌形象一致。""".format(
                    product_website=product_website,
                    product_details=product_details
                ),

            expected_output="""一份详尽的 Instagram 营销活动文档，
                包含清晰的目标、目标受众策略、
                内容指南、标签策略、发布建议和成功指标。""",
            agent=agent,

            # === 任务上下文（依赖关系）===
            # 此任务依赖前两个任务的输出
            # CrewAI 会自动将 product_analysis 和 competitor_analysis 
            # 的结果传入此任务作为参考
            context=[
                self.product_analysis,
                self.competitor_analysis,
            ],
        )

    def instagram_ad_copy(self, agent):
        """
        任务4：撰写 Instagram 广告文案（最终输出之一）
        
        目的：根据营销策略创作可直接发布的 Instagram 帖子文案
        
        执行代理：creative_content_creator_agent（创意文案撰稿人）
        
        特点：
            - 不需要 product_website 和 product_details 参数
            - 通过 context 自动获取前序任务的所有分析和策划结果
            - 这是文案团队的最终产出任务
        
        输出内容：
            - 吸引人的标题/钩子
            - 正文文案（符合 Instagram 风格）
            - 相关的 hashtags（10-30 个）
            - 适当的表情符号
            - 行动号召 (CTA)
        """
        return Task(
            description="""
                利用所有可用的研究和策略见解，创作引人入胜且有效的
                Instagram 广告文案。
                
                文案应包含以下要素：
                
                1. **吸引人的标题**：立即抓住注意力
                2. **引人入胜的正文**：
                   - 清晰传达产品的价值主张
                   - 使用适合目标受众的语言和语调
                   - 讲述引起共鸣的故事或传达强有力的信息
                   - 保持简洁但有力
                3. **相关标签**：混合流行、小众和品牌特定标签
                   以最大化触达和参与度（10-30 个标签）
                4. **行动号召 (CTA)**：明确的下一步指引
                5. **表情符号**：适当使用以增加视觉吸引力和个性
                
                确保文案与品牌形象一致，并与已制定的营销策略保持一致。""",

            expected_output="""准备好发布的完整 Instagram 广告帖子，
                包括标题、带有相关标签的正文、行动号召和表情符号。
                文案应引人入胜、具有说服力，并针对最大参与度进行优化。""",

            agent=agent,

            # 依赖前面的营销策划任务，获取策略指导
            context=[self.campaign_development],
        )

    # ================================================================
    #                 图片团队任务 (Image Crew Tasks)
    # ================================================================

    def take_photograph_task(self, agent, ad_copy, product_website, product_details):
        """
        任务5：拍摄/构思画面描述（最终输出之二）
        
        目的：根据广告文案生成 AI 绘图的提示词（Prompt）
        
        执行代理：senior_photographer_agent（高级摄影师）
        
        参数:
            agent:           高级摄影代理
            ad_copy:         任务4生成的 Instagram 文案（重要输入！）
            product_website: 产品网站 URL
            product_details: 额外产品信息
            
        工作原理：
            摄影师阅读 ad_copy → 理解文案的情感和主题
            → 用专业的摄影术语描述画面构图
            → 输出的描述可作为 Midjourney / DALL-E / Stable Diffusion 的提示词
            
        输出内容：
            - 详细的画面描述（英文，适合 AI 绘图工具）
            - 构图说明（主体位置、角度）
            - 光线描述（自然光/人工光、方向）
            - 色彩方案
            - 风格参考（如：电影感、极简主义等）
        """
        return Task(
            description="""根据以下 Instagram 广告文案，拍摄一张令人惊叹的照片：
                
                --- AD COPY START ---
                {ad_copy}
                --- AD COPY END ---
                
                产品网站：{product_website}
                额外详情：{product_details}
                
                根据广告文案，创作一张能够完美捕捉帖子精髓的照片。
                考虑以下几点：
                
                1. **视觉概念**：创造性地解读文案的核心信息和情感
                2. **构图**：精心安排画面元素以获得最大冲击力
                3. **光线**：使用能够增强预期情绪的光照条件
                4. **调色板**：选择与品牌形象互补的色彩方案
                5. **风格**：采用与产品和目标受众一致的审美风格
                6. **细节**：添加能提升整体效果的细微细节
                
                提供一张高质量、专业级的照片，讲述故事并唤起情感。""".format(
                    ad_copy=ad_copy,
                    product_website=product_website,
                    product_details=product_details,
                ),

            expected_output="""一张高质量、专业级照片的详细 Midjourney 或 DALL-E 提示词，
                完美捕捉 Instagram 帖子的精髓，包括视觉概念、
                构图、光照、调色板和风格元素的详细描述。""",

            agent=agent,
        )

    def review_photo(self, agent, product_website, product_details):
        """
        任务6：审核和优化图片描述（质量控制环节）
        
        目的：确保摄影师输出的图片描述达到专业标准
        
        执行代理：chief_creative_diretor_agent（首席创意总监）
        
        工作原理：
            创意总监审查 take_photograph_task 的输出
            → 从艺术性和品牌一致性角度进行评估
            → 如有必要则提出修改意见或重新生成
            
        为什么需要这个任务？
            - 作为"人肉过滤器"，保证输出质量
            - 模拟真实创意团队的工作流（初稿 → 审核 → 定稿）
            - 确保最终图片描述可用于 AI 绘图工具
        
        返回:
            经过审核和优化的最终图片描述/Prompt
        """
        return Task(
            description="""审查摄影师拍摄的图片，确保它符合最高艺术标准，
                并完美契合 Instagram 帖子的预期概念。
                
                产品网站：{product_website}
                额外详情：{product_details}
                
                在你的审查过程中，请考虑：
                
                1. **视觉冲击力**：图像是否立即抓住注意力？
                2. **概念一致性**：它是否很好地传达了预期的信息？
                3. **技术质量**：构图、光照和执行是否专业？
                4. **品牌契合度**：它是否符合品牌形象和价值主张？
                5. **情感共鸣**：它是否能唤起目标受众的期望情感？
                6. **创新性**：它是否提供了新鲜独特的视角？
                
                如果图像符合标准，批准它并提供简要理由。
                如果需要改进，提供具体的反馈和建议。""".format(
                    product_website=product_website,
                    product_details=product_details,
                ),

            expected_output="""对所提供图片的详细审查，
                包括对其优势和潜在改进领域的评估，
                以及关于其在 Instagram 营销活动中适用性的最终决定。""",

            agent=agent,

            # 依赖前面摄影师的任务，审核其输出
            context=[self.take_photograph_task],
        )
