#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""=================================================
@PROJECT_NAME: agent_example
@File    : model_provider.py
@Author  : Liuyz
@Date    : 2024/6/28 17:12
@Function: 

@Modify History:
         
@Copyright：Copyright(c) 2024-2026. All Rights Reserved
=================================================="""
import os, json
import dashscope
from prompt import user_prompt
from dashscope.api_entities.dashscope_response import Message


class ModelProvider(object):
    def __init__(self):
        self.api_key = os.environ.get('DASH_SCOPE_API_KEY')
        self.model_name = os.environ.get('MODEL_NAME')
        self._client = dashscope.Generation()
        self.max_retry_time = 3

    def chat(self, prompt, chat_history):
        """
        call_llm
            1、sys_prompt
            2、user_prompt
            3、history
        """
        cur_retry_time = 0
        while cur_retry_time < self.max_retry_time:
            cur_retry_time += 1
            try:
                """
                role 是消息的角色，通常用于标识消息的来源。在对话系统中，role 通常有以下几种常见值：
                user：表示消息是由用户发送的
                assistant：表示消息是由助手（例如 AI 模型）发送的
                system: 表示系统级别的消息。这些消息通常由系统发送，用于提供上下文、指令或配置信息，而不是直接与用户或助手进行交互。
                """
                messages = [Message(role="system", content=prompt)]
                for history in chat_history:
                    messages.append(Message(role="user", content=history[0]))
                    messages.append(Message(role="system", content=history[1]))
                # 最后1条信息是用户的输入
                messages.append(Message(role="user", content=user_prompt))

                response = self._client.call(
                    model=self.model_name,
                    api_key=self.api_key,
                    messages=messages
                )

                print("response:{}".format(response))
                content = json.loads(response["output"]["text"])
                return content
            except Exception as e:
                print("call llm exception:{}".format(e))
        return {}
