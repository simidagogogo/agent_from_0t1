"""
# File        : multi_turn_conversation.py
# Author      : Shard Zhang
# Date        : 2025/6/12 21:22
# Brief       : 
# Attention   : 
"""

import os
from dashscope import Generation
import dashscope
from dotenv import load_dotenv

load_dotenv()

def get_response(messages):
    response = Generation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASH_SCOPE_API_KEY"),
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen-plus",
        messages=messages,
        result_format="message",
    )
    return response


if __name__ == '__main__':
    # 初始化一个 messages 数组
    messages = [
        {
            "role": "system",
            "content": """
            你是一名阿里云百炼手机商店的店员，你负责给用户推荐手机。
            手机有两个参数：屏幕尺寸（包括6.1英寸、6.5英寸、6.7英寸）、分辨率（包括2K、4K）。
            你一次只能向用户提问一个参数。
            如果用户提供的信息不全，你需要反问他，让他提供没有提供的参数。
            对于当前问到的参数, 一定要确认用户确认后, 才可以问下一个参数. 一定要等用户完全确认完参数后, 才算参数收集完成.
            如果参数收集完成，你要说：我已了解您的购买意向，请稍等。
            """,
        }
    ]

    assistant_output = "欢迎光临阿里云百炼手机商店，您需要购买什么尺寸的手机呢？"
    print(f"模型输出：{assistant_output}\n")
    while "我已了解您的购买意向" not in assistant_output:
        user_input = input("请输入：")

        # 将用户问题信息添加到messages列表中
        messages.append({"role": "user", "content": user_input})

        # 获取大模型的回复信息
        assistant_output = get_response(messages).output.choices[0].message.content

        # 将大模型的回复信息添加到messages列表中
        messages.append({"role": "assistant", "content": assistant_output})
        print(f"模型输出：{assistant_output}")
        print("\n")
