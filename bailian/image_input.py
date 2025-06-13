"""
# File        : image_input.py
# Author      : Shard Zhang
# Date        : 2025/6/13 10:43
# Brief       : 
# Attention   : 
"""

import os
import dashscope
from dotenv import load_dotenv

load_dotenv()

messages = [
    {
        "role": "user",
        "content": [
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"},
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
            {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/rabbit.png"},
            {"text": "这些是什么?"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    api_key=os.environ.get('DASH_SCOPE_API_KEY', ''),
    model='qwen-vl-max', # 此处以qwen-vl-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages
    )
print(response)
print(response.output.choices[0].message.content[0]['text']) # type: ignore