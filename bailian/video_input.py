"""
# File        : video_input.py
# Author      : Shard Zhang
# Date        : 2025/6/13 11:15
# Brief       : 
# Attention   : 
"""

from http import HTTPStatus
import os
# dashscope版本需要不低于1.20.10
import dashscope
from dotenv import load_dotenv

load_dotenv()

messages = [
    {
        "role": "user",
        "content": [
            {"video":["https://img.alicdn.com/imgextra/i3/O1CN01K3SgGo1eqmlUgeE9b_!!6000000003923-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01BjZvwg1Y23CF5qIRB_!!6000000003000-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i4/O1CN01Ib0clU27vTgBdbVLQ_!!6000000007859-0-tps-3840-2160.jpg",
                        "https://img.alicdn.com/imgextra/i1/O1CN01aygPLW1s3EXCdSN4X_!!6000000005710-0-tps-3840-2160.jpg"]
            },
            {"text": "描述这个视频的具体过程"}
        ]
    }
]

if __name__ == '__main__':
    response = dashscope.MultiModalConversation.call(
        api_key=os.getenv("DASH_SCOPE_API_KEY"),
        model='qwen-vl-max-latest',  # 此处以qwen-vl-max-latest为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages
    )

    if response.status_code == HTTPStatus.OK:
        print(response)
        print(response.output.choices[0].message.content[0]['text'])
    else:
        print(response.code)
        print(response.message)