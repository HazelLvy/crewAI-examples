# AI 团队 - 落地页生成器
## 简介
本项目是一个使用 CrewAI 框架的示例，用于自动化**从单一创意想法生成完整落地页（Landing Page）**的流程。CrewAI 编排自主 AI 代理，使它们能够协作并高效地执行复杂任务。

*免责声明：模板文件未包含在内，因为它们是 Tailwind 模板。如果你有许可证，可以从 [Tailwind UI](https://tailwindui.com/templates) 下载并将单独的模板文件夹放入 `./templates` 目录中。模板引用配置在 `config/templates.json` 中。本项目未测试过其他模板，如需使用可能需要修改 `tasks.py` 中的提示词。*

由 [@joaomdmoura](https://x.com/joaomdmoura) 创作

- [CrewAI 框架](#crewai-框架)
- [运行脚本](#运行脚本)
- [详细说明](#详细说明)
- [使用 GPT 3.5](#使用-gpt-35)
- [使用 Ollama 本地模型](#使用-ollama-本地模型)
- [贡献](#贡献)
- [支持与联系](#支持与联系)
- [许可证](#许可证)

## CrewAI 框架
CrewAI 旨在促进角色扮演 AI 代理之间的协作。在本示例中，这些代理协同工作，通过**扩展创意想法、选择模板、并定制化调整**，将一个想法转化为一个完整的落地页。

## 运行脚本
默认使用 **GPT-4**，因此你需要有 GPT-4 的访问权限才能运行。

***免责声明：** 除非你修改配置，否则默认会使用 gpt-4，这将会产生费用（约 2-9 美元）。完整运行大约需要 10-45 分钟。好好享受这段空闲时间吧！*

- **配置环境**：复制 `.env.example` 并设置 [Browserless](https://www.browserless.io/)、[Serper](https://serper.dev/) 和 [OpenAI](https://platform.openai.com/api-keys) 的环境变量。
- **安装依赖**：运行 `poetry install --no-root`。
- **添加 Tailwind 模板**：将 Tailwind 单独的模板文件夹放入 `./templates` 目录。如果你有许可证，可从 [Tailwind UI](https://tailwindui.com/templates) 下载。模板引用在 `config/templates.json` 中配置。注意：未测试过其他模板，使用其他模板时可能需要修改 `tasks.py` 中的提示词。
- **执行脚本**：运行 `poetry run python main.py` 并输入你的创意想法。

## 详细说明
- **运行脚本**：执行 `python main.py` 并在提示时输入你的创意想法。该脚本将利用 CrewAI 框架处理想法并生成落地页。
- **输出**：生成的落地页将被打包为 `workdir.zip` 文件供你下载。
- **关键组件**：
  - `./main.py`: 主脚本文件。
  - `./tasks.py`: 包含任务提示的主文件。
  - `./tools`: 包含代理使用的工具类。
  - `./config`: 代理的配置文件。
  - `./templates`: 存放 Tailwind 模板的目录（未包含在项目中）。

## 使用 GPT 3.5
CrewAI 允许你向代理构造函数传递 `llm` 参数，这将成为代理的"大脑"。因此，将代理从 GPT-4 切换到 GPT-3.5 非常简单——只需在使用该 LLM 的代理上传递此参数即可（在 `main.py` 中）：

```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model='gpt-3.5') # 加载 GPT-3.5

self.idea_analyst = Agent(
    **idea_analyst_config,
    verbose=True,
    llm=llm, # <----- 在此处传入我们的 LLM 引用
    tools=[
        SearchTools.search_internet,
        BrowserTools.scrape_and_summarize_website
    ]
)
```

## 使用 Ollama 本地模型
CrewAI 框架支持与本地模型（如 Ollama）集成，以增强灵活性和定制能力。这允许你使用自己的模型，对于专业任务或数据隐私问题特别有用。

### 设置 Ollama
- **安装 Ollama**：确保在你的环境中正确安装了 Ollama。请遵循 Ollama 提供的安装指南获取详细说明。
- **配置 Ollama**：设置 Ollama 以配合本地模型工作。你可能需要[使用 Modelfile 调整模型](https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md)，建议添加 `Observation` 作为停止词（stop word），并尝试调整 `top_p` 和 `temperature` 参数。

### 将 Ollama 集成到 CrewAI
- **实例化 Ollama 模型**：创建 Ollama 模型的实例。你可以在实例化时指定模型名称和基础 URL。例如：

```python
from langchain.llms import Ollama
ollama_openhermes = Ollama(model="agent")
```

- **将 Ollama 模型传递给代理**：在 CrewAI 框架内创建代理时，可以将 Ollama 模型作为参数传递给 Agent 构造函数。例如：

```python
self.idea_analyst = Agent(
    **idea_analyst_config,
    verbose=True,
    llm=ollama_openhermes, # 在此处传入 Ollama 模型
    tools=[
        SearchTools.search_internet,
        BrowserTools.scrape_and_summarize_website
    ]
)
```

### 使用本地模型的优势
- **隐私性**：本地模型允许在你自己的基础设施内处理数据，确保数据隐私。
- **定制性**：你可以根据任务的特定需求自定义模型。
- **性能**：取决于你的硬件配置，本地模型可以提供性能优势，尤其是在延迟方面。

## 许可证
本项目基于 MIT 许可证发布。
