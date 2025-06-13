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
        {'role': 'user', 'content': 'KFC有几种吃法?'}
    ]

    response = dashscope.Generation.call(
        api_key=api_key,
        model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=messages,
        # result_format参数不可以设置为"text"。
        result_format='message'
    )

    print("=" * 20 + "思考过程" + "=" * 20)
    print(response.output.choices[0].message.reasoning_content)
    print("=" * 20 + "最终答案" + "=" * 20)
    print(response.output.choices[0].message.content)