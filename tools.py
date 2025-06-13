#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@PROJECT_NAME: agent_example
@File    : tools.py
@Author  : Liuyz
@Date    : 2024/6/28 14:45
@Function: action的实现, 统一称为tools
    1、写文件
    2、读文件
    3、追加的方式写
    4、专业领域知识的获取(网络搜索)
"""

import json
import os
# from langchain_community.tools.tavily_search import TavilySearchResults

def _get_workdir_root():
    workdir_root = os.environ.get('WORKDIR_ROOT', "./data/llm_result")
    return workdir_root

WORKDIR_ROOT = _get_workdir_root()

def read_file(filename) -> str:
    filename = os.path.join(WORKDIR_ROOT, filename)
    if not os.path.exists(filename):
        return f"{filename} not exit, please check file exist before read"

    with open(filename, 'r', encoding="utf-8") as f:
        return "\n".join(f.readlines())


def append_to_file(filename, content) -> str:
    filename = os.path.join(WORKDIR_ROOT, filename)
    if not os.path.exists(filename):
        return f"{filename} not exit, please check file exist before read"

    with open(filename, 'a') as f:
        f.write(content)
    return "append_content to file success."


def write_to_file(filename, content) -> str:
    filename = os.path.join(WORKDIR_ROOT, filename)
    if not os.path.exists(WORKDIR_ROOT):
        os.makedirs(WORKDIR_ROOT)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return "write content to file success."


def search(query) -> str:
    """
    :param query:
    :return:
    """
    daily = TavilySearchResults(max_results=5)
    try:
        ret = daily.invoke(input=query)
        print("搜索结果:{}".format(ret))
        content_list = []
        # ret = [{"content": "", "url": ""}]
        for obj in ret:
            content_list.append(obj["content"])
        return "\n".join(content_list)
    except Exception as e:
        return "search error:{}".format(e)


# 工具信息
tools_info = [
    {
        "name": "read_file",
        "description": "read file from agent generate, should write file before read",
        "args": [
            {
                "name": "filename",
                "type": "string",
                "description": "read file name"
            }
        ]
    },
    {
        "name": "append_to_file",
        "description": "append llm content to file, should write file before read",
        "args":
            [
                {
                    "name": "filename",
                    "type": "string",
                    "description": "file name"
                },
                {
                    "name": "content",
                    "type": "string",
                    "description": "append to file content"
                }
            ]
    },
    {
        "name": "write_to_file",
        "description": "write llm content to file",
        "args": [
            {
                "name": "filename",
                "type": "string",
                "description": "file name"
            },
            {
                "name": "content",
                "type": "string",
                "description": "write to file content"
            }
        ]
    },
    {
        "name": "finish",
        "description": "完成用户目标",
        "args": [
            {
                "name": "answer",
                "type": "string",
                "description": "最后的目标结果"
            }
        ]
    },
    {
        "name": "search",
        "description": "this is a search engine, you can gain additional knowledge though this search engine when you are unsure of large model return",
        "args": [
            {
                "name": "query",
                "type": "string",
                "description": "search query to look up"
            }
        ]
    }
]

# action-name到函数的映射 map -> {"action_name" : func}
tools_map = {
    "read_file": read_file,
    "append_to_file": append_to_file,
    "write_to_file": write_to_file,
    "search": search
}

def gen_desc(arr) -> str:
    return "\n".join([f"{idx + 1}.{con}" for idx, con in enumerate(arr)])

def gen_tools_desc() -> str:
    """
    生成工具描述
    :return: str
    """
    tools_desc = []
    for idx, tool in enumerate(tools_info):
        args_desc = []
        # print(f"tool: {tool}")
        for info in tool['args']:
            args_desc.append(
                {
                    "name": info["name"],
                    "description": info["description"],
                    "type": info["type"]
                }
            )
        args_desc = json.dumps(args_desc, ensure_ascii=False)
        tool_desc = f"{idx + 1}. {tool['name']}: {tool['description']}, args: {args_desc}"
        tools_desc.append(tool_desc)
    tools_prompt = "\n".join(tools_desc)
    return tools_prompt
