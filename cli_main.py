#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@File    : cli_main.py
@Author  : shard zhang
@Date    : 2024/6/28 14:04
@Function: agent核心逻辑调用
        1、环境变量的设置
        2、工具的引入
        3、prompt模板
        4、模型的初始化
"""

import time
from tools import tools_map
from prompt import gen_prompt, user_prompt
from model_provider import ModelProvider
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
mp = ModelProvider()


def parse_thoughts(response):
    try:
        thoughts = response.get("thoughts")
        observation = response.get("observation")
        plan = thoughts.get("plan")
        reasoning = thoughts.get("reasoning")
        criticism = thoughts.get("criticism")
        observation = thoughts.get("speak")
        prompt = f"plan: {plan}\n reasoning: {reasoning}\n criticism: {criticism}\n observation: {observation}"
        return prompt
    except Exception as e:
        print("parse_thoughts error:{}".format(e))
        return "".format(e)


def agent_execute(query, max_request_time=10):
    chat_history = []  # [user, assis]
    agent_scratch = ""
    cur_request_time = 0
    while cur_request_time < max_request_time:
        cur_request_time += 1
        print('********* {}.开始调用大模型....'.format(cur_request_time))
        start_time = time.time()
        prompt = gen_prompt(query, agent_scratch)
        response = mp.chat(prompt, chat_history)
        end_time = time.time()
        print('********* {}.结束调用大模型....花费时间:{}'.format(cur_request_time, end_time - start_time))

        # 大模型输出结果的处理
        if not response or not isinstance(response, dict):
            print("call llm exception, 即将重试, response is: {}".format(response))
            continue

        # 这里统一叫tools
        action_info = response.get("action")
        action_name = action_info.get("name")
        action_args = action_info.get("args")
        print("action_name: {}, action_args: {}".format(action_name, action_args))

        # 其他输出信息
        thoughts = response.get("thoughts")
        plan = thoughts.get("plan")
        reasoning = thoughts.get("reasoning")
        criticism = thoughts.get("criticism")
        observation = thoughts.get("speak")
        print("observation:{}".format(observation))
        print("plan:{}".format(plan))
        print("reasoning:{}".format(reasoning))
        print("criticism:{}".format(criticism))

        if action_name == "finish":
            final_answer = action_args.get("answer")
            print("final_answer: {}".format(final_answer))
            break

        # speak
        observation = response.get("observation")
        observation = response.get("thoughts").get("speak")

        try:
            func = tools_map.get(action_name)
            call_function_result = func(**action_args)
        except Exception as e:
            print("调用工具异常: {}".format(e))
            call_function_result = "{}".format(e)

        agent_scratch = f"{agent_scratch} \n observation: {observation} \n execute action result: {call_function_result}"
        user_msg = "根据给定的目标和迄今为止取得的进展，确定下一个要执行action，并使用前面指定的JSON模式进行响应："
        assistant_msg = parse_thoughts(response)
        chat_history.append([user_msg, assistant_msg])

    if cur_request_time == max_request_time:
        print("本次任务执行失败!")
    else:
        print("本次任务成功！")


def main():
    # 支持用户的多次需要输入和交互
    while True:
        query = input("请输入您的目标:")
        if query == "exit":
            return
        agent_execute(query, max_request_time=10)


if __name__ == '__main__':
    main()
