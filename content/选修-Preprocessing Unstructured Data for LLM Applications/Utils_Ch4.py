import os
from dotenv import load_dotenv, find_dotenv

# 获取 Unstructured API 相关环境变量
class Utils:
  def __init__(self):
    pass
  def get_dlai_api_key(self):
    _ = load_dotenv(find_dotenv())
    return os.getenv("DLAI_API_KEY")
    
  def get_dlai_url(self):
    _ = load_dotenv(find_dotenv())
    return os.getenv("DLAI_API_URL")
