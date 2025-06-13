# -*- coding: UTF-8 -*-
#!/usr/bin/env python

"""
@File    : prompt.py
@Author  : Liuyz
@Date    : 2024/6/28 15:58
@Function: 
        prompt包含的功能:
            1、任务描述
            2、工具描述
            3、用户输入user_msg:
            4、assistant_msg:
            5、结果限制
            6、更好实践描述
"""

from tools import gen_tools_desc, gen_desc

# 限制条件
constraints = [
    "仅使用下面列出的动作",
    "你只能主动行动，在计划行动时需要考虑这一点",
    "你无法与物理对象交互,如果对于完成任务或目标是绝对必要，则必须要求用户为你完成，如果用户拒绝，并且没有办法实现目标，则直接终止，避免浪费时间和精力。"
]

# 资源说明
resources = [
    "提供搜索和信息收集的互联网接入",
    "读取和写入文件的能力",
    "你是一个大语言模型，接受了大量文本的训练，包括大量的事实知识，利用这些知识避免不必要的信息收集"
]

# 最佳实践
best_practices = [
    "不断地回顾和分析你的行为，确保发挥你最大的能力",
    "不断地进行建设性的自我批评",
    "反思你过去的决策和策略，完善你的方案",
    "每个动作执行都有代价，所以要聪明高效，目的是用最少的步骤完成任务",
    "利用你的信息收集能力来寻找你不知道的信息"
]

#  prompt模板
prompt_template = """
你是一个问答专家，你必须始终独立做出决策，无需寻求用户的帮助，发挥你作为LLM的优势，追求简答的策略，不要涉及法律的问题。

目标: 
{query}

限制条件说明: 
{constraints_prompt}

动作说明: 这是你唯一可使用的动作，你的任何操作都必须通过以下操作实现: 
{actions_prompt}

资源说明: 
{resources_prompt}

最佳实践说明: 
{best_practices_prompt}

agent_scratch: 
{agent_scratch}

你应该以json格式响应, 响应格式如下: 
{response_format_prompt}
确保响应结果可以由python json.loads()成功加载。
"""

# 响应格式
response_format_prompt = """
    {
        "action": {
            "name": "action name",
            "args": {
                "args name": "args value"
            }
        },
        "thoughts":{
            "plan": "简单的描述短期和长期的计划列表",
            "criticism": "建设性的自我批评",
            "speak": "当前步骤返回给用户的总结",
            "reasoning": "推理"
        },
        "observation": "观察当前任务的整体进度"
    }
"""

def gen_prompt(query, agent_scratch):
    """
    prompt包含的功能:
        1、任务的描述
        2、工具的描述
        3、用户输入user_msg:
        4、assistant_msg:
        5、结果的限制
        6、给出更好实践的描述
    :param query:
    :param agent_scratch: 存储智能体的中间状态或观察结果, 包含智能体的思考过程、计划plan、批评criticism、推理reasoning等信息
    :return:
    """
    actions_prompt = gen_tools_desc()
    constraints_prompt = gen_desc(constraints)
    resources_prompt = gen_desc(resources)
    best_practices_prompt = gen_desc(best_practices)
    prompt = prompt_template.format(
        query=query,
        constraints_prompt=constraints_prompt,
        actions_prompt=actions_prompt,
        resources_prompt=resources_prompt,
        best_practices_prompt=best_practices_prompt,
        response_format_prompt=response_format_prompt,
        agent_scratch=agent_scratch
    )
    return prompt
