#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: image2text_chat.py
@time: 2025/6/10 15:51
@project: llm-cookbook
@desc: 基于硅基流动的图生文模型加载
"""

import re
import warnings
from enum import Enum

warnings.filterwarnings("ignore", category=DeprecationWarning)

import base64
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import imghdr

loaded = load_dotenv(find_dotenv(), override=True)
# 从环境变量中获取 OpenAI API Key 或者直接赋值
API_KEY = os.getenv("API_KEY")

# 从环境变量中获取 BASE_URL，默认使用硅基流动
BASE_URL = os.getenv("BASE_URL", "https://api.siliconflow.cn/v1")

# 基于openai的OpenAI实例
openai_client = OpenAI(api_key=API_KEY, base_url=BASE_URL, max_retries=3)


class InputImageType(Enum):
    IMAGE_URL = 'IMAGE_URL'
    IMAGE_BASE64 = 'IMAGE_BASE64'
    IMAGE_FILE = 'IMAGE_FILE'


def get_completion(input_image_type, image_input, text_input=None, model_endpoint="Qwen/Qwen2.5-VL-72B-Instruct"):
    """
    从图像中提取文本信息。
    :param image_input: 图像输入，可以是图片路径或图片 URL
    :param text_input: 文字输入
    :param model_endpoint: 模型名称
    """
    text_input = text_input or "请用一段文字描述这张图片。"

    image_info = {
        "type": "image_url",
        "image_url": {
            "type": "image_url",
            "image_url": {
                "url": "URL_ADDRESS",
                "detail": "auto"
            }
        }
    }

    if input_image_type == InputImageType.IMAGE_FILE:
        # 传入的是图片文件
        base64_image = image_to_base64(image_input)
        # 获取图片的 MIME 类型
        mime_type = get_image_mime_type(image_input)
        image_info = {
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime_type};base64,{base64_image}",
                "detail": "auto"
            }
        }
    if input_image_type == InputImageType.IMAGE_URL:
        # 传入的是图片 URL
        image_info = {
            "type": "image_url",
            "image_url": {
                "url": image_input,
                "detail": "auto"
            }
        }
    if input_image_type == InputImageType.IMAGE_BASE64:
        # 传入的是图片的base64编码
        image_info = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{image_input}",
                "detail": "auto"
            }
        }

    # 构造包含图像信息的消息
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text_input
                },
                image_info
            ]
        }
    ]

    response = openai_client.chat.completions.create(model=model_endpoint,
                                                     messages=messages,
                                                     n=1, temperature=0, seed=42,
                                                     presence_penalty=0, frequency_penalty=0,
                                                     max_tokens=4096
                                                     )

    return response.choices[0].message.content.strip()


def image_to_base64(image_path):
    """
    将指定路径的图片转换为 Base64 编码字符串。

    :param image_path: 图片文件的路径
    :return: 图片的 Base64 编码字符串，如果出现异常则返回 None
    """
    try:
        with open(image_path, "rb") as image_file:
            # 读取图片文件内容
            image_data = image_file.read()
            # 将图片内容转换为 Base64 编码
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            return base64_encoded
    except Exception as e:
        print(f"转换图片到 Base64 编码时出错: {e}")
        return None


def get_image_mime_type(image_path):
    """
    获取图片的 MIME 类型。

    :param image_path: 图片文件的路径
    :return: 图片的 MIME 类型，如果无法识别则返回 'jpeg'
    """
    image_type = imghdr.what(image_path)
    if image_type:
        return f"image/{image_type}"
    return "image/jpeg"


def is_url(string):
    """
    判断字符串是否为有效的 URL
    :param string: 输入的字符串
    :return: 如果是 URL 则返回 True，否则返回 False
    """
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// 或 https:// 或 ftp:// 或 ftps://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # 域名
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP 地址
        r'(?::\d+)?'  # 可选的端口号
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(url_pattern, string) is not None


if __name__ == '__main__':
    image_url = "https://free-images.com/sm/9596/dog_animal_greyhound_983023.jpg"
    content = "请描述图片，并生成10个字以内的标题。"
    print(get_completion(InputImageType.IMAGE_URL ,image_url))
