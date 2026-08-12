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
```

2. 加载模型  
如果需要调用模型，请直接在notebook中添加以下代码（注意需要加载项目根目录到环境的path中），不需要额外的配置。
```python
import os
from dotenv import load_dotenv, find_dotenv

loaded = load_dotenv(find_dotenv(), override=True)
# 从环境变量中获取 OpenAI API Key 或者直接赋值
API_KEY = os.getenv("API_KEY")

# Read the model settings from the environment.
BASE_URL = os.getenv("BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
```

## MiniMax configuration reference

Set `MODEL_NAME` and `BASE_URL` in `.env` when using the MiniMax API:

```text
API_KEY=your_api_key
MODEL_NAME=MiniMax-M3
BASE_URL=https://api.minimax.io/v1
```

Choose the endpoint that matches the account region and client protocol:

| Region | OpenAI-compatible endpoint | Anthropic-compatible endpoint | Documentation |
| --- | --- | --- | --- |
| Global | `https://api.minimax.io/v1` | `https://api.minimax.io/anthropic` | `https://platform.minimax.io/docs` |
| China | `https://api.minimaxi.com/v1` | `https://api.minimaxi.com/anthropic` | `https://platform.minimaxi.com/docs` |

Current model metadata and pricing in USD per million tokens:

| Model | Context window | Input modalities | Thinking modes | Input | Output | Cache read | Cache write |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: |
| `MiniMax-M3` | 1,000,000 | text, image, video | adaptive, disabled | $0.60 | $2.40 | $0.12 | Not listed |
| `MiniMax-M2.7` | 204,800 | text | always on | $0.30 | $1.20 | $0.06 | $0.375 |
