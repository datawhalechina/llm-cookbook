#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: chat_robot.py
@time: 2025/6/12 19:42
@project: llm-cookbook
@desc: 
"""
import datetime
import os

import panel as pn
import param
import requests
import wikipedia
from dotenv import load_dotenv, find_dotenv
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_tool_messages
from langchain.agents.output_parsers import ToolsAgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain.tools import tool
from langchain_core.runnables import RunnablePassthrough
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

loaded = load_dotenv(find_dotenv(), override=True)
# 从环境变量中获取 OpenAI API Key 或者直接赋值
API_KEY = os.getenv("API_KEY")
# 从环境变量中获取 BASE_URL，默认使用硅基流动
BASE_URL = os.getenv("BASE_URL", "https://api.siliconflow.cn/v1")

pn.extension()


# 定义维基百科搜索的tool
@tool
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[: 3]:  # 取前三个页面标题
        try:
            # 使用 wikipedia 模块的 page 函数，获取指定标题的维基百科页面对象。
            wiki_page = wikipedia.page(title=page_title, auto_suggest=False)
            # 获取页面摘要
            summaries.append(f"页面: {page_title}\n摘要: {wiki_page.summary}")
        except (
                wikipedia.exceptions.PageError,
                wikipedia.exceptions.DisambiguationError,
        ):
            pass
    if not summaries:
        return "维基百科没有搜索到合适的结果"
    return "\n\n".join(summaries)


# 定义输入格式
class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="要获取天气数据的位置的纬度")
    longitude: float = Field(..., description="要获取天气数据的位置的经度")


# 使用 @tool 装饰器并指定输入格式
@tool(args_schema=OpenMeteoInput)
def get_current_temperature(latitude: float, longitude: float):
    """"根据给定的坐标位置获得温度"""

    # Open Meteo API 的URL
    open_meteo_url = "https://api.open-meteo.com/v1/forecast"

    # 请求参数
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    # 发送 API 请求
    response = requests.get(open_meteo_url, params=params)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析 JSON 响应
        results = response.json()
    else:
        # 处理请求失败的情况
        raise Exception(f"API Request failed with status code: {response.status_code}")

    # 获取当前 UTC 时间
    current_utc_time = datetime.datetime.now(datetime.UTC)

    # 将时间字符串转换为 datetime 对象
    time_list = [datetime.datetime.fromisoformat(time_str).replace(tzinfo=datetime.timezone.utc) for time_str in
                 results['hourly']['time']]

    # 获取温度列表
    temperature_list = results['hourly']['temperature_2m']

    # 找到最接近当前时间的索引
    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))

    # 获取当前温度
    current_temperature = temperature_list[closest_time_index]

    # 返回当前温度的字符串形式
    return f'现在温度是 {current_temperature}°C'


# 自定义的工具（自由发挥）
@tool
def create_your_own(query: str) -> str:
    """可以自定义的功能函数 """
    print(type(query))
    return query[::-1]


# 将之前定义的工具加入工具列表
tools = [get_current_temperature, search_wikipedia, create_your_own]

CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME", os.getenv("MODEL_NAME", "Qwen/Qwen3-8B"))

chat_model = ChatOpenAI(temperature=0.01, model_name=CHAT_MODEL_NAME, max_tokens=4096,
                        openai_api_key=API_KEY, openai_api_base=BASE_URL, max_retries=3,
                        seed=42, presence_penalty=0.1, frequency_penalty=0.1,
                        )


# 定义 cbfs 类
class cbfs(param.Parameterized):

    # 初始化函数
    def __init__(self, _tools, **params):
        super(cbfs, self).__init__(**params)
        self.answer = None
        self.panels = []  # 存储 GUI 面板
        self.functions = [convert_to_openai_function(f) for f in _tools]  # 将tools格式化为 OpenAI 函数
        self.tools = [{"type": "function", "function": x} for x in self.functions]
        self.model = chat_model.bind(tools=self.tools)  # 创建 ChatOpenAI 模型
        self.memory = ConversationBufferMemory(return_messages=True,
                                               memory_key="chat_history")  # 创建 ConversationBufferMemory
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are helpful but sassy assistant"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])  # 创建 ChatPromptTemplate
        self.chain = RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_to_tool_messages(x["intermediate_steps"])
        ) | self.prompt | self.model | ToolsAgentOutputParser()  # 创建处理链
        self.qa = AgentExecutor(agent=self.chain, tools=tools, verbose=False, memory=self.memory)  # 创建 AgentExecutor

    # 对话链函数
    def convchain(self, query):
        if not query:
            return
        inp.value = ''
        result = self.qa.invoke({"input": query})
        self.answer = result['output']
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query, width=450)),
            pn.Row('ChatBot:', pn.pane.Markdown(self.answer, width=450, styles={'background-color': '#F6F6F6'}))
        ])
        return pn.WidgetBox(*self.panels, scroll=True)

    # 清除历史记录函数
    def clr_history(self, count=0):
        self.panels = []  # 清空存储对话面板的列表
        self.memory.clear()  # 清空对话记忆
        return pn.WidgetBox(scroll=True, height=400, width=539)  # 返回清空后的对话面板


# 创建 cbfs 对象，传递工具列表
cb = cbfs(tools)

# 创建文本输入框组件
inp = pn.widgets.TextInput(placeholder='请输入文本...')

# 创建发送按钮
send_button = pn.widgets.Button(name='发送', button_type='primary')

# 创建清空会话记录按钮
clear_button = pn.widgets.Button(name='清空会话', button_type='danger')

# 初始对话面板
conversation = pn.WidgetBox(scroll=True, height=400, width=539)


# 定义发送消息的函数
def send_message(event):
    query = inp.value
    if query:
        result = cb.convchain(query)
        conversation.objects += result.objects
        inp.value = ''  # 清空输入框


def handle_enter_event(event):
    if inp.value != '':
        send_message(event)


# 监听回车事件
inp.param.watch(handle_enter_event, 'enter_pressed')


# 定义清空会话记录的函数
def clear_conversation(event):
    print(event)
    result = cb.clr_history()
    conversation.objects = result.objects


# 将按钮点击事件与发送消息函数绑定
send_button.on_click(send_message)

# 将按钮点击事件与清空会话记录函数绑定
clear_button.on_click(clear_conversation)

# 创建仪表板，包含标题、输入框、发送按钮和对话记录面板
dashboard = pn.Column(
    pn.pane.Markdown('# 对话机器人'),  # 显示标题
    pn.Row(inp, send_button, clear_button),  # 显示文本输入框和发送按钮
    pn.layout.Divider(),
    pn.panel(conversation, loading_indicator=True),  # 显示对话链面板
    pn.layout.Divider(),
)

dashboard.show()
