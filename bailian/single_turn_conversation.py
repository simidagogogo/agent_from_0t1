"""
# File        : single_turn_conversation_deepseek.py
# Author      : Shard Zhang
# Date        : 2025/6/12 16:55
# Brief       : 
# Attention   : 
"""
import os
import dashscope
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("DASH_SCOPE_API_KEY")

if __name__ == '__main__':
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ]

    response = dashscope.Generation.call(
        api_key=api_key,
        model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        result_format='message',
        temperature=0.7,
        )
    print(response.output.choices[0].message.content)