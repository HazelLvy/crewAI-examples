# AI 团队 - Instagram 帖子生成
## 简介
本项目是一个使用 CrewAI 框架的示例，用于自动化生成 Instagram 帖子的流程。CrewAI 编排自主 AI 代理，使它们能够协作并高效地执行复杂任务。

#### Instagram 帖子
[![Instagram 帖子](https://img.youtube.com/vi/lcD0nT8IVTg/0.jpg)](https://www.youtube.com/watch?v=lcD0nT8IVTg "Instagram 帖子")

由 [@joaomdmoura](https://x.com/joaomdmoura) 创作

- [CrewAI 框架](#crewai-框架)
- [运行脚本](#运行脚本)
- [详细说明](#详细说明)
- [使用 Ollama 本地模型](#使用-ollama-本地模型)
- [许可证](#许可证)

## CrewAI 框架
CrewAI 旨在促进角色扮演 AI 代理之间的协作。在本示例中，这些代理协同工作以生成富有创意且流行的 Instagram 帖子。

## 运行脚本
本示例默认通过 Ollama 使用 OpenHermes 2.5，因此你需要下载 [Ollama](ollama.ai) 和 [OpenHermes](https://ollama.ai/library/openhermes)。

你可以通过修改 `.env` 文件中的 `MODEL` 环境变量来更改模型。

- **配置环境**：复制 `.env.example` 并设置 [Browseless](https://www.browserless.io/)、[Serper](https://serper.dev/) 的环境变量。
- **安装依赖**：运行 `poetry install --no-root`（使用 crewAI==0.130.0）。
- **执行脚本**：运行 `python main.py` 并输入你的创意想法。

## 详细说明
- **运行脚本**：执行 `python main.py` 并在提示时输入你的创意想法。该脚本将利用 CrewAI 框架处理想法并生成 Instagram 帖子。
- **关键组件**：
  - `./main.py`: 主脚本文件。
  - `./tasks.py`: 包含任务提示的主文件。
  - `./agents.py`: 包含代理创建的主文件。
  - `./tools/`: 包含代理使用的工具类。

## 使用 Ollama 本地模型
本示例完全使用本地模型运行。CrewAI 框架支持与闭源模型和本地模型的集成，通过使用 Ollama 等工具，提供增强的灵活性和定制能力。这允许你使用自己的模型，对于专业任务或数据隐私问题特别有用。

### 设置 Ollama
- **安装 Ollama**：确保在你的环境中正确安装了 Ollama。请遵循 Ollama 提供的安装指南获取详细说明。
- **配置 Ollama**：设置 Ollama 以配合本地模型工作。你可能需要[使用 Modelfile 调整模型](https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md)，我建议尝试调整 `top_p` 和 `temperature` 参数。

## 许可证
本项目基于 MIT 许可证发布。
