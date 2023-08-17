import openai
import os
from dotenv import load_dotenv, find_dotenv


# 如果你设置的是全局的环境变量，这行代码则没有任何作用。
_ = load_dotenv(find_dotenv())

# 获取环境变量 OPENAI_API_KEY
openai.api_key = os.environ['OPENAI_API_KEY']

# 一个封装 OpenAI 接口的函数，参数为 Prompt，返回对应结果


def get_completion(prompt,
                   model="gpt-3.5-turbo"
                   ):
    '''
    prompt: 对应的提示词
    model: 调用的模型，默认为 gpt-3.5-turbo(ChatGPT)。你也可以选择其他模型。
           https://platform.openai.com/docs/models/overview
    '''

    messages = [{"role": "user", "content": prompt}]

    # 调用 OpenAI 的 ChatCompletion 接口
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message["content"]


def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=500):
    '''
    prompt: 对应的提示词
    model: 调用的模型，默认为 gpt-3.5-turbo(ChatGPT)。你也可以选择其他模型。
           https://platform.openai.com/docs/models/overview
    temperature: 模型输出的随机程度。默认为0，表示输出将非常确定。增加温度会使输出更随机。
    max_tokens: 定模型输出的最大的 token 数。
    '''

    # 调用 OpenAI 的 ChatCompletion 接口
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message["content"]
