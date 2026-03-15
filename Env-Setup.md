# 项目环境配置

## 安装项目依赖包

1. 基础环境：Python3.12+

2. 安装UV
```shell
pip install uv
set UV_INDEX=https://mirrors.aliyun.com/pypi/simple
```

3. 安装Python依赖包
```shell
uv sync --python 3.12 --all-extras
```

4. 切换到本地环境(.venv)，请安装whl包
```shell
cd .venv/Scripts
activate
```

## 启动Jupyter编辑器

```shell
jupyter notebook
```

## 模型加载

1. 在项目根目录下新建`.env`文件，并添加以下内容
```text
API_KEY=your_api_key
BASE_URL=model_base_url
MODEL_NAME=model_name
```

2. 加载模型
如果需要调用模型，请直接在notebook中添加以下代码（注意需要加载项目根目录到环境的path中），不需要额外的配置。
```python
import os
from dotenv import load_dotenv, find_dotenv

loaded = load_dotenv(find_dotenv(), override=True)
# 从环境变量中获取配置
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.siliconflow.cn/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen3-8B")
```

## 支持的 LLM 提供商

本项目基于 OpenAI 兼容 API 接口，支持多种 LLM 提供商。只需在 `.env` 中配置对应的 `API_KEY`、`BASE_URL` 和 `MODEL_NAME` 即可切换。

### 硅基流动（默认）

```text
API_KEY=your_siliconflow_api_key
BASE_URL=https://api.siliconflow.cn/v1
MODEL_NAME=Qwen/Qwen3-8B
```

### MiniMax

[MiniMax](https://www.minimaxi.com/) 提供兼容 OpenAI 的 API 接口，支持 MiniMax-M2.5 等模型，最大支持 204K 上下文窗口。

```text
API_KEY=your_minimax_api_key
BASE_URL=https://api.minimax.io/v1
MODEL_NAME=MiniMax-M2.5
```

可选模型：`MiniMax-M2.5`（完整版）、`MiniMax-M2.5-highspeed`（高速版）。

### OpenAI

```text
API_KEY=your_openai_api_key
BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o
```

### 其他兼容 OpenAI 接口的提供商

任何支持 OpenAI 兼容 API 的提供商都可以通过配置 `BASE_URL` 来使用，例如 DeepSeek、智谱 AI 等。