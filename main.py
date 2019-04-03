# -*- coding: utf-8 -*-
# @Time    : 2019-04-03 19:22:24
# @Author  : Nismison
# @FileName: main.py
# @Description: 微信聊天机器人
# @Blog    ：https://blog.tryfang.cn

import itchat
from requests import get

index = 0       # 用于记录接收到的消息是第几条
username_list = []      # 用于存放消息发送方的username


def dict_get(dict_, objkey):
    """
    从嵌套的字典中拿到需要的值
    """
    for key, value in dict_.items():
        if key == objkey:
            return value
        else:
            # 如果value是dict类型，则迭代
            if isinstance(value, dict):
                ret = dict_get(value, objkey)
                if ret is not None:
                    return ret
            # 如果value是list类型，则取第0个进行迭代
            elif isinstance(value, list):
                ret = dict_get(value[0], objkey)
                if ret is not None:
                    return ret
    # 如果找不到指定的key，返回None
    return None


def turling_connect(text, app_key):
    """
    将文本发送到机器人接口
    """
    api_url = "http://api.ruyi.ai/v1/message?q={}&app_key={}&user_id=".format(text, app_key)
    response = get(api_url).json()
    res = dict_get(response, "text")
    return res


@itchat.msg_register(itchat.content.TEXT)
def reply(msg):
    """
    微信消息自动回复
    """
    global index
    # 如果接收到的消息是对方发送的第一条消息，发送提示语句，避免机器人坏事，如果不需要的话请删除，仅保留最后一行即可
    if index == 0 and msg.fromUserName not in username_list:
        index += 1
        username_list.append(msg.fromUserName)
        return "嗨~我是机器人哟，我的主人正在睡觉，如果有急事的话请直接电话联系哈~当然你也可以跟我聊天哈哈~~"
    else:
        index += 1
        return turling_connect(text=msg.text, app_key="Your AppKey")


if __name__ == "__main__":
    itchat.auto_login(hotReload=True)
    itchat.run()
