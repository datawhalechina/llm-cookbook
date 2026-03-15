#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: langchain_chat.py
@time: 2025/6/10 15:55
@project: llm-cookbook
@desc: 
"""
import os

from dotenv import load_dotenv, find_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI

loaded = load_dotenv(find_dotenv(), override=True)
# 从环境变量中获取 OpenAI API Key 或者直接赋值
API_KEY = os.getenv("API_KEY")

# 从环境变量中获取 BASE_URL，默认使用硅基流动
BASE_URL = os.getenv("BASE_URL", "https://api.siliconflow.cn/v1")

# 从环境变量中获取模型名称
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME", os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3"))
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-m3")

# 基于langchain的OpenAI实例，用于代码生成
chat_model = ChatOpenAI(temperature=0.01, model_name=CHAT_MODEL_NAME, max_tokens=4096,
                        openai_api_key=API_KEY, openai_api_base=BASE_URL, max_retries=3,
                        seed=42, presence_penalty=0.1, frequency_penalty=0.1,
                        )

embedding_model = OpenAIEmbeddings(
    openai_api_key=API_KEY,
    openai_api_base=BASE_URL,
    model=EMBEDDING_MODEL_NAME
)