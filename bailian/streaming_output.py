"""
# File        : streaming_output.py
# Author      : Shard Zhang
# Date        : 2025/6/12 21:33
# Brief       : 
# Attention   : 
"""

import os
import dashscope
from dotenv import load_dotenv

load_dotenv()

messages = [
    {'role': 'system', 'content': 'you are a helpful assistant'},
    {'role': 'user', 'content': '你是谁？'}
]

if __name__ == '__main__':
    responses = dashscope.Generation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv('DASH_SCOPE_API_KEY'),
        model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        result_format='message',
        stream=True,
        incremental_output=True,
        temperature=0.8,
    )

    full_text = ""
    for response in responses:
        content = response.output.choices[0].message.content
        full_text += content
    print(full_text)