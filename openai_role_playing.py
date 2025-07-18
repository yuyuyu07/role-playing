import os  # 操作系统交互接口的库
from openai import OpenAI  # 从openai库里导入OpenAI类

# --- 创建函数 ---
def get_gemini_response(api_key,messages_history: list):
    # 创建OpenAI实例
    client = OpenAI(
        api_key=api_key,  # 使用传入的API密钥
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # 使用传入的API地址
    )

    # 调用.chat.completions.create()方法
    response = client.chat.completions.create(
        model="gemini-2.5-flash-lite-preview-06-17",  # 使用传入的模型名称
        messages=messages_history,  # 使用传入的聊天列表
        temperature=0.8,  # 温度参数，控制生成文本的随机性
    )

    # 提取 生成文本内容
    AI助手 = response.choices[0].message.role  # 响应对象.选项数组[0].消息.assistant
    生成内容 = response.choices[0].message.content  # 响应对象.选项数组[0].消息.内容

    return {"role": AI助手, "content": 生成内容}  # 返回AI的回复
