#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""=================================================
@PROJECT_NAME: agent_example
@File    : bailian.py
@Author  : Liuyz
@Date    : 2024/6/28 16:43
@Function: 
=================================================="""

import random
from http import HTTPStatus
import dashscope
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("DASH_SCOPE_API_KEY")

def call_stream_with_messages():
    is_stream = True
    messages = [{'role': 'user', 'content': '用萝卜、土豆、茄子做饭，给我个菜谱'}]
    responses = dashscope.Generation.call(
        model='qwen1.5-110b-chat',
        messages=messages,
        seed=random.randint(1, 10000),  # set the random seed, optional, default to 1234 if not set
        result_format='message',  # set the result to be "message"  format.
        stream=is_stream,   #  set to True to get streaming output. 关键!
        incremental_output=True,  # get streaming output incrementally.\
        api_key=api_key
    )

    if not is_stream:
        print(f"responses: {responses}")
        print(f"content: {responses.output.choices[0].message.content}")
    else:
        full_content = ''
        idx = 1
        for response in responses:
            idx += 1
            if response.status_code == HTTPStatus.OK:
                content = response.output.choices[0]['message']['content']
                full_content += content
                print(f"idx:{idx}. {content}")
            else:
                print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message
                ))
    print('Full content: \n' + full_content)


if __name__ == '__main__':
    call_stream_with_messages()
