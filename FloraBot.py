from flask import Flask, request
from websocket_server import WebsocketServer, WebSocketHandler
import logging
from socketserver import TCPServer
import requests
import importlib.util
import os
import json
import threading
import sys
import subprocess
import platform
import time
import random
import re
import zipfile
import shutil

flora_logo = "\x1b[38;2;37;197;127m█\x1b[38;2;38;197;127m█\x1b[38;2;39;197;128m█\x1b[38;2;40;197;129m█\x1b[38;2;41;197;130m█\x1b[38;2;42;197;131m█\x1b[38;2;43;197;132m█\x1b[38;2;45;197;133m╗\x1b[38;2;46;197;134m \x1b[38;2;47;197;135m█\x1b[38;2;48;197;136m█\x1b[38;2;49;197;137m╗\x1b[38;2;50;197;138m \x1b[38;2;51;197;139m \x1b[38;2;53;197;140m \x1b[38;2;54;197;141m \x1b[38;2;55;197;142m \x1b[38;2;56;197;143m \x1b[38;2;57;197;144m \x1b[38;2;58;197;145m \x1b[38;2;59;197;146m \x1b[38;2;61;197;147m \x1b[38;2;62;197;148m \x1b[38;2;63;197;149m \x1b[38;2;64;197;150m \x1b[38;2;65;197;151m \x1b[38;2;66;197;152m \x1b[38;2;67;197;153m \x1b[38;2;69;197;154m \x1b[38;2;70;197;155m \x1b[38;2;71;197;156m \x1b[38;2;72;197;157m \x1b[38;2;73;197;158m \x1b[38;2;74;197;159m \x1b[38;2;76;197;160m \x1b[38;2;77;197;161m \x1b[38;2;78;197;162m \x1b[38;2;79;197;163m \x1b[38;2;80;197;164m█\x1b[38;2;81;197;165m█\x1b[38;2;82;197;166m█\x1b[38;2;84;197;167m█\x1b[38;2;85;197;168m█\x1b[38;2;86;197;169m█\x1b[38;2;87;197;170m╗\x1b[38;2;88;197;171m \x1b[38;2;89;197;172m \x1b[38;2;90;197;173m \x1b[38;2;92;197;174m \x1b[38;2;93;197;175m \x1b[38;2;94;197;176m \x1b[38;2;95;197;177m \x1b[38;2;96;197;178m \x1b[38;2;97;197;179m \x1b[38;2;98;197;180m \x1b[38;2;100;197;181m \x1b[38;2;101;197;182m \x1b[38;2;102;197;183m \x1b[38;2;103;197;184m \x1b[38;2;104;197;185m \x1b[38;2;105;197;186m \x1b[38;2;107;197;187m \x1b[0m\n\x1b[38;2;37;197;127m█\x1b[38;2;38;197;127m█\x1b[38;2;39;197;128m╔\x1b[38;2;40;197;129m═\x1b[38;2;41;197;130m═\x1b[38;2;42;197;131m═\x1b[38;2;43;197;132m═\x1b[38;2;45;197;133m╝\x1b[38;2;46;197;134m \x1b[38;2;47;197;135m█\x1b[38;2;48;197;136m█\x1b[38;2;49;197;137m║\x1b[38;2;50;197;138m \x1b[38;2;51;197;139m \x1b[38;2;53;197;140m \x1b[38;2;54;197;141m \x1b[38;2;55;197;142m \x1b[38;2;56;197;143m \x1b[38;2;57;197;144m \x1b[38;2;58;197;145m \x1b[38;2;59;197;146m \x1b[38;2;61;197;147m \x1b[38;2;62;197;148m \x1b[38;2;63;197;149m \x1b[38;2;64;197;150m \x1b[38;2;65;197;151m \x1b[38;2;66;197;152m \x1b[38;2;67;197;153m \x1b[38;2;69;197;154m \x1b[38;2;70;197;155m \x1b[38;2;71;197;156m \x1b[38;2;72;197;157m \x1b[38;2;73;197;158m \x1b[38;2;74;197;159m \x1b[38;2;76;197;160m \x1b[38;2;77;197;161m \x1b[38;2;78;197;162m \x1b[38;2;79;197;163m \x1b[38;2;80;197;164m█\x1b[38;2;81;197;165m█\x1b[38;2;82;197;166m╔\x1b[38;2;84;197;167m═\x1b[38;2;85;197;168m═\x1b[38;2;86;197;169m█\x1b[38;2;87;197;170m█\x1b[38;2;88;197;171m╗\x1b[38;2;89;197;172m \x1b[38;2;90;197;173m \x1b[38;2;92;197;174m \x1b[38;2;93;197;175m \x1b[38;2;94;197;176m \x1b[38;2;95;197;177m \x1b[38;2;96;197;178m \x1b[38;2;97;197;179m \x1b[38;2;98;197;180m \x1b[38;2;100;197;181m \x1b[38;2;101;197;182m \x1b[38;2;102;197;183m█\x1b[38;2;103;197;184m█\x1b[38;2;104;197;185m╗\x1b[38;2;105;197;186m \x1b[38;2;107;197;187m \x1b[0m\n\x1b[38;2;37;197;127m█\x1b[38;2;38;197;127m█\x1b[38;2;39;197;128m█\x1b[38;2;40;197;129m█\x1b[38;2;41;197;130m█\x1b[38;2;42;197;131m╗\x1b[38;2;43;197;132m \x1b[38;2;45;197;133m \x1b[38;2;46;197;134m \x1b[38;2;47;197;135m█\x1b[38;2;48;197;136m█\x1b[38;2;49;197;137m║\x1b[38;2;50;197;138m \x1b[38;2;51;197;139m \x1b[38;2;53;197;140m \x1b[38;2;54;197;141m█\x1b[38;2;55;197;142m█\x1b[38;2;56;197;143m█\x1b[38;2;57;197;144m█\x1b[38;2;58;197;145m╗\x1b[38;2;59;197;146m \x1b[38;2;61;197;147m \x1b[38;2;62;197;148m \x1b[38;2;63;197;149m█\x1b[38;2;64;197;150m█\x1b[38;2;65;197;151m█\x1b[38;2;66;197;152m█\x1b[38;2;67;197;153m╗\x1b[38;2;69;197;154m \x1b[38;2;70;197;155m \x1b[38;2;71;197;156m█\x1b[38;2;72;197;157m█\x1b[38;2;73;197;158m█\x1b[38;2;74;197;159m█\x1b[38;2;76;197;160m╗\x1b[38;2;77;197;161m \x1b[38;2;78;197;162m \x1b[38;2;79;197;163m \x1b[38;2;80;197;164m█\x1b[38;2;81;197;165m█\x1b[38;2;82;197;166m█\x1b[38;2;84;197;167m█\x1b[38;2;85;197;168m█\x1b[38;2;86;197;169m█\x1b[38;2;87;197;170m╔\x1b[38;2;88;197;171m╝\x1b[38;2;89;197;172m \x1b[38;2;90;197;173m \x1b[38;2;92;197;174m█\x1b[38;2;93;197;175m█\x1b[38;2;94;197;176m█\x1b[38;2;95;197;177m█\x1b[38;2;96;197;178m╗\x1b[38;2;97;197;179m \x1b[38;2;98;197;180m \x1b[38;2;100;197;181m█\x1b[38;2;101;197;182m█\x1b[38;2;102;197;183m█\x1b[38;2;103;197;184m█\x1b[38;2;104;197;185m█\x1b[38;2;105;197;186m█\x1b[38;2;107;197;187m╗\x1b[0m\n\x1b[38;2;37;197;127m█\x1b[38;2;38;197;127m█\x1b[38;2;39;197;128m╔\x1b[38;2;40;197;129m═\x1b[38;2;41;197;130m═\x1b[38;2;42;197;131m╝\x1b[38;2;43;197;132m \x1b[38;2;45;197;133m \x1b[38;2;46;197;134m \x1b[38;2;47;197;135m█\x1b[38;2;48;197;136m█\x1b[38;2;49;197;137m║\x1b[38;2;50;197;138m \x1b[38;2;51;197;139m \x1b[38;2;53;197;140m█\x1b[38;2;54;197;141m█\x1b[38;2;55;197;142m╔\x1b[38;2;56;197;143m═\x1b[38;2;57;197;144m█\x1b[38;2;58;197;145m█\x1b[38;2;59;197;146m╗\x1b[38;2;61;197;147m \x1b[38;2;62;197;148m█\x1b[38;2;63;197;149m█\x1b[38;2;64;197;150m╔\x1b[38;2;65;197;151m═\x1b[38;2;66;197;152m═\x1b[38;2;67;197;153m╝\x1b[38;2;69;197;154m \x1b[38;2;70;197;155m█\x1b[38;2;71;197;156m█\x1b[38;2;72;197;157m╔\x1b[38;2;73;197;158m═\x1b[38;2;74;197;159m█\x1b[38;2;76;197;160m█\x1b[38;2;77;197;161m╗\x1b[38;2;78;197;162m \x1b[38;2;79;197;163m \x1b[38;2;80;197;164m█\x1b[38;2;81;197;165m█\x1b[38;2;82;197;166m╔\x1b[38;2;84;197;167m═\x1b[38;2;85;197;168m═\x1b[38;2;86;197;169m█\x1b[38;2;87;197;170m█\x1b[38;2;88;197;171m╗\x1b[38;2;89;197;172m \x1b[38;2;90;197;173m█\x1b[38;2;92;197;174m█\x1b[38;2;93;197;175m╔\x1b[38;2;94;197;176m═\x1b[38;2;95;197;177m█\x1b[38;2;96;197;178m█\x1b[38;2;97;197;179m╗\x1b[38;2;98;197;180m \x1b[38;2;100;197;181m \x1b[38;2;101;197;182m╚\x1b[38;2;102;197;183m█\x1b[38;2;103;197;184m█\x1b[38;2;104;197;185m╔\x1b[38;2;105;197;186m═\x1b[38;2;107;197;187m╝\x1b[0m\n\x1b[38;2;37;197;127m█\x1b[38;2;38;197;127m█\x1b[38;2;39;197;128m║\x1b[38;2;40;197;129m \x1b[38;2;41;197;130m \x1b[38;2;42;197;131m \x1b[38;2;43;197;132m \x1b[38;2;45;197;133m \x1b[38;2;46;197;134m \x1b[38;2;47;197;135m█\x1b[38;2;48;197;136m█\x1b[38;2;49;197;137m█\x1b[38;2;50;197;138m╗\x1b[38;2;51;197;139m \x1b[38;2;53;197;140m╚\x1b[38;2;54;197;141m█\x1b[38;2;55;197;142m█\x1b[38;2;56;197;143m█\x1b[38;2;57;197;144m█\x1b[38;2;58;197;145m╔\x1b[38;2;59;197;146m╝\x1b[38;2;61;197;147m \x1b[38;2;62;197;148m█\x1b[38;2;63;197;149m█\x1b[38;2;64;197;150m║\x1b[38;2;65;197;151m \x1b[38;2;66;197;152m \x1b[38;2;67;197;153m \x1b[38;2;69;197;154m \x1b[38;2;70;197;155m╚\x1b[38;2;71;197;156m█\x1b[38;2;72;197;157m█\x1b[38;2;73;197;158m█\x1b[38;2;74;197;159m█\x1b[38;2;76;197;160m█\x1b[38;2;77;197;161m█\x1b[38;2;78;197;162m╗\x1b[38;2;79;197;163m \x1b[38;2;80;197;164m█\x1b[38;2;81;197;165m█\x1b[38;2;82;197;166m█\x1b[38;2;84;197;167m█\x1b[38;2;85;197;168m█\x1b[38;2;86;197;169m█\x1b[38;2;87;197;170m╔\x1b[38;2;88;197;171m╝\x1b[38;2;89;197;172m \x1b[38;2;90;197;173m╚\x1b[38;2;92;197;174m█\x1b[38;2;93;197;175m█\x1b[38;2;94;197;176m█\x1b[38;2;95;197;177m█\x1b[38;2;96;197;178m╔\x1b[38;2;97;197;179m╝\x1b[38;2;98;197;180m \x1b[38;2;100;197;181m \x1b[38;2;101;197;182m \x1b[38;2;102;197;183m█\x1b[38;2;103;197;184m█\x1b[38;2;104;197;185m█\x1b[38;2;105;197;186m╗\x1b[38;2;107;197;187m \x1b[0m\n\x1b[38;2;37;197;127m╚\x1b[38;2;38;197;127m═\x1b[38;2;39;197;128m╝\x1b[38;2;40;197;129m \x1b[38;2;41;197;130m \x1b[38;2;42;197;131m \x1b[38;2;43;197;132m \x1b[38;2;45;197;133m \x1b[38;2;46;197;134m \x1b[38;2;47;197;135m╚\x1b[38;2;48;197;136m═\x1b[38;2;49;197;137m═\x1b[38;2;50;197;138m╝\x1b[38;2;51;197;139m \x1b[38;2;53;197;140m \x1b[38;2;54;197;141m╚\x1b[38;2;55;197;142m═\x1b[38;2;56;197;143m═\x1b[38;2;57;197;144m═\x1b[38;2;58;197;145m╝\x1b[38;2;59;197;146m \x1b[38;2;61;197;147m \x1b[38;2;62;197;148m╚\x1b[38;2;63;197;149m═\x1b[38;2;64;197;150m╝\x1b[38;2;65;197;151m \x1b[38;2;66;197;152m \x1b[38;2;67;197;153m \x1b[38;2;69;197;154m \x1b[38;2;70;197;155m \x1b[38;2;71;197;156m╚\x1b[38;2;72;197;157m═\x1b[38;2;73;197;158m═\x1b[38;2;74;197;159m═\x1b[38;2;76;197;160m═\x1b[38;2;77;197;161m═\x1b[38;2;78;197;162m╝\x1b[38;2;79;197;163m \x1b[38;2;80;197;164m╚\x1b[38;2;81;197;165m═\x1b[38;2;82;197;166m═\x1b[38;2;84;197;167m═\x1b[38;2;85;197;168m═\x1b[38;2;86;197;169m═\x1b[38;2;87;197;170m╝\x1b[38;2;88;197;171m \x1b[38;2;89;197;172m \x1b[38;2;90;197;173m \x1b[38;2;92;197;174m╚\x1b[38;2;93;197;175m═\x1b[38;2;94;197;176m═\x1b[38;2;95;197;177m═\x1b[38;2;96;197;178m╝\x1b[38;2;97;197;179m \x1b[38;2;98;197;180m \x1b[38;2;100;197;181m \x1b[38;2;101;197;182m \x1b[38;2;102;197;183m╚\x1b[38;2;103;197;184m═\x1b[38;2;104;197;185m═\x1b[38;2;105;197;186m╝\x1b[38;2;107;197;187m \x1b[0m\n"
flora_server = Flask("FloraBot", template_folder="FloraBot", static_folder="FloraBot")
connection_type = "HTTP"
flora_host = "127.0.0.1"
flora_port = 3003
framework_address = "127.0.0.1:3000"
bot_id = 0
administrator = []
auto_install = False

flora_version = "V1.12 Beta"
big_update = False
update_content = """内置功能:
1. /帮助  -  若不知道 FloraBot 有哪些功能, 请试试使用该指令
2. 若不知道一个插件有哪些功能, 请试试使用该指令
3. /检查更新  -  验性功能, 检查 FloraBot 是否有新的版本可更新, 并且引导你进行下一步更新
4. /插件列表  -  将该指令移出仅 Bot 管理员可用指令"""

plugins_dict = {}  # 插件对象字典
plugins_info_dict = {}  # 插件信息字典
flora_help_dict = {
    "Flora": {
        "Help": [
            {
                "Class": "基础功能",
                "Commands": [
                    {
                        "Command": "/帮助",
                        "Content": "若不知道 FloraBot 有哪些功能, 请试试使用该指令"
                    },
                    {
                        "Command": "/帮助 + [空格] + [插件名]",
                        "Content": "若不知道一个插件有哪些功能, 请试试使用该指令"
                    }
                ]
            },
            {
                "Class": "插件相关",
                "Commands": [
                    {
                        "Command": "/插件列表",
                        "Content": "查看已添加的插件以及插件的禁启用状态"
                    }
                ]
            },
            {
                "Class": "插件管理(仅 Bot 管理员可用)",
                "AdminUse": True,
                "Commands": [
                    {
                        "Command": "/重载插件",
                        "Content": "若未找到插件, 但插件文件已添加, 请试试使用该指令"
                    },
                    {
                        "Command": "/启用插件 + [空格] + [插件名]",
                        "Content": "启用一个处于禁用状态的插件"
                    },
                    {
                        "Command": "/禁用插件 + [空格] + [插件名]",
                        "Content": "禁用一个处于启用状态的插件"
                    }
                ]
            },
            {
                "Class": "调试与测试(仅 Bot 管理员可用)",
                "AdminUse": True,
                "Commands": [
                    {
                        "Command": "/echo + [空格] + [内容]",
                        "Content": "测试 Bot 是否正常工作, 让 Bot 账号复述一遍内容"
                    },
                    {
                        "Command": "/echo1 + [空格] + [内容]",
                        "Content": "与 /echo 功能一致, 复述不为回复"
                    },
                    {
                        "Command": "/API测试 + [空格] + [API(终结点, 不要带上\"/\")] + [空格] + 参数 + [空格] + [参数(Json格式)]",
                        "Content": "测试调用框架的 API, 后面的\"参数\"部分可选(根据 API 而定, 有的 API 无需参数)"
                    }
                ]
            },
            {
                "Class": "更新 FloraBot (仅 Bot 管理员可用)",
                "AdminUse": True,
                "Commands": [
                    {
                        "Command": "/检查更新",
                        "Content": "实验性功能, 检查 FloraBot 是否有新的版本可更新, 并且引导你进行下一步更新"
                    }
                ]
            }
        ]
    }
}
help_info_dict = {}


def load_config():  # 加载FloraBot配置文件函数
    global auto_install, connection_type, flora_host, flora_port, framework_address, bot_id, administrator
    if not os.path.isdir("./FloraBot"):
        os.makedirs("./FloraBot")
    if not os.path.isdir("./FloraBot/Plugins"):
        os.makedirs("./FloraBot/Plugins")
    if os.path.isdir("./FloraBot/UpdateCache"):
        shutil.rmtree("./FloraBot/UpdateCache")
    if os.path.isfile("./Config.json"):  # 若文件存在
        with open("./Config.json", "r", encoding="UTF-8") as read_flora_config:
            flora_config = json.loads(read_flora_config.read())
        auto_install = flora_config.get("AutoInstallLibraries")
        connection_type = flora_config.get("ConnectionType")
        flora_api.update({"ConnectionType": connection_type})
        flora_host = flora_config.get("FloraHost")
        flora_api.update({"FloraHost": flora_host})
        flora_port = flora_config.get("FloraPort")
        flora_api.update({"FloraPort": flora_port})
        framework_address = flora_config.get("FrameworkAddress")
        flora_api.update({"FrameworkAddress": framework_address})
        bot_id = flora_config.get("BotID")
        flora_api.update({"BotID": bot_id})
        administrator = flora_config.get("Administrator")
        flora_api.update({"Administrator": administrator})
    else:  # 若文件不存在
        print("FloraBot 启动失败, 未找到配置文件 Config.json")
        with open("./Config.json", "w", encoding="UTF-8") as write_flora_config:
            write_flora_config.write(json.dumps({"AutoInstallLibraries": True, "ConnectionType": "HTTP", "FloraHost": "127.0.0.1", "FloraPort": 3003, "FrameworkAddress": "127.0.0.1:3000", "BotQQ": 0, "Administrator": [0]}, ensure_ascii=False, indent=4))
        print("已生成一个新的配置文件 Config.json , 请修改后再次启动 FloraBot")
        exit()


def send_msg(send_type: str, msg: str, uid: str | int, gid: str | int | None, mid: str | int | None = None, ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):
    # 发送消息函数,send_type: 发送类型,决定是用HTTP还是WebSocket发送消息
    # msg: 正文,uid: ID,gid: 群号,mid: 消息编号
    # ws_client: WebSocket连接实例,ws_server: WebSocket服务端实例(若发送类型为WebSocket这两个参数必填)
    # send_host: HTTP协议发送地址,send_port: HTTP协议发送端口(若填这两个参数则使用自定义地址发送)
    if send_type == "HTTP":
        send_address = framework_address
        if send_host != "" and send_port != "":
            send_address = f"{send_host}:{send_port}"
        url = f"http://{send_address}"
        data = {}
        if mid is not None:  # 当消息编号不为None时,则发送的消息为回复
            data.update({"message": f"[CQ:reply,id={mid}]{msg}"})
        else:  # 反之为普通消息
            data.update({"message": msg})
        if gid is not None:  # 当群号不为None时,则发送给群聊
            url += f"/send_group_msg"
            data.update({"group_id": gid})
        else:  # 反之为私聊
            url += f"/send_private_msg"
            data.update({"user_id": uid})
        try:
            return requests.post(url, json=data, timeout=5).json()  # 提交发送消息
        except requests.exceptions.RequestException:
            pass
    elif send_type == "WebSocket":
        data = {}
        send_params = {}
        if mid is not None:  # 当消息编号不为None时,则发送的消息为回复
            send_params.update({"message": f"[CQ:reply,id={mid}]{msg}"})
        else:  # 反之为普通消息
            send_params.update({"message": msg})
        if gid is not None:  # 当群号不为None时,则发送给群聊
            data.update({"action": "send_group_msg"})
            send_params.update({"group_id": gid})
        else:  # 反之为私聊
            data.update({"action": "send_private_msg"})
            send_params.update({"user_id": uid})
        data.update({"params": send_params})
        try:
            if ws_server is not None and ws_client is not None:
                ws_server.send_message(ws_client, json.dumps(data, ensure_ascii=False))
                random_num = random.random()
                call_api_return.append(random_num)
                while random_num not in call_api_returned:
                    if exit_flag:
                        break
                    time.sleep(0.1)
                if exit_flag:
                    return None
                else:
                    return call_api_returned.pop(random_num)
        except ConnectionError:
            return None
        except TypeError:
            return None


def call_api(send_type: str, api: str, params: dict, ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):
    # 发送消息函数,send_type: 发送类型,决定是用HTTP还是WebSocket发送消息
    # api: 接口(str类型), data: 数据(dict类型)
    # ws_client: WebSocket连接实例,ws_server: WebSocket服务端实例(若发送类型为WebSocket这两个参数必填)
    # send_host: HTTP协议发送地址,send_port: HTTP协议发送端口(若填这两个参数则使用自定义地址发送)
    if send_type == "HTTP":
        send_address = framework_address
        if send_host != "" and send_port != "":
            send_address = f"{send_host}:{send_port}"
        try:
            return requests.post(f"http://{send_address}/{api}", json=params, timeout=5).json()  # 提交发送消息
        except requests.exceptions.RequestException:
            return None
    elif send_type == "WebSocket":
        try:
            if ws_server is not None and ws_client is not None:
                ws_server.send_message(ws_client, json.dumps({"action": api, "params": params}, ensure_ascii=False))
                random_num = random.random()
                call_api_return.append(random_num)
                while random_num not in call_api_returned:
                    if exit_flag:
                        break
                    time.sleep(0.1)
                if exit_flag:
                    return None
                else:
                    return call_api_returned.pop(random_num)
        except ConnectionError:
            return None
        except TypeError:
            return None


def install_libraries(libraries_name: str):
    if importlib.util.find_spec(libraries_name) is None:
        print(f"正在安装 {libraries_name} 库...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", libraries_name])
            print(f"{libraries_name} 库安装完成")
        except subprocess.CalledProcessError:
            print(f"{libraries_name} 库安装失败")


def load_plugins():  # 加载插件函数
    print("正在加载插件, 请稍后...")
    help_info_dict.clear()
    help_info_dict.update(flora_help_dict)
    plugins_info_dict.clear()
    plugins_dict.clear()
    for plugin in os.listdir("./FloraBot/Plugins"):  # 遍历所有插件
        plugin_path = f"FloraBot/Plugins/{plugin}"
        if os.path.isfile(f"./{plugin_path}/Plugin.json"):
            with open(f"./{plugin_path}/Plugin.json", "r", encoding="UTF-8") as read_plugin_config:
                plugin_config = json.loads(read_plugin_config.read())
            if os.path.isfile(f"./{plugin_path}/{plugin_config.get('MainPyName')}.py") and plugin_config.get("EnablePlugin"):  # 如果配置正确则导入插件
                plugin_config = plugin_config.copy()
                print(f"正在加载插件 {plugin_config.get('PluginName')} ...")
                plugin_config.update({"ThePluginPath": plugin_path})
                plugins_info_dict.update({plugin_config.get("PluginName"): plugin_config})  # 添加插件信息
                if plugin_config.get("Help") is not None:
                    help_info_dict.update({"Plugins": {plugin_config.get("PluginName"): {"Help": plugin_config.get("Help")}}})
                if auto_install and plugin_config.get("DependentLibraries") is not None:
                    print("已开启自动安装依赖库, 正在安装插件所依赖的库...")
                    for libraries_name in plugin_config.get("DependentLibraries"):
                        install_libraries(libraries_name)
                spec = importlib.util.spec_from_file_location(plugin_config.get("MainPyName"), f"./{plugin_path}/{plugin_config.get('MainPyName')}.py")
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except ModuleNotFoundError as error_info:
                    if auto_install:
                        install_libraries(str(error_info).split("'")[1])
                        spec.loader.exec_module(module)
                    else:
                        raise ModuleNotFoundError(error_info)
                try:
                    module.flora_api = flora_api.copy()  # 传入API参数
                except AttributeError:
                    pass
                module.flora_api.update({"ThePluginPath": plugin_path})
                try:
                    threading.Thread(target=module.init).start()  # 开线程初始化插件
                except AttributeError:
                    pass
                plugins_dict.update({plugin_config.get("PluginName"): module})  # 添加插件对象
    update_flora_api()


def broadcast_event(data: dict, send_type: str, ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):
    # 广播消息函数,data: 基于OneBot协议的数据
    # send_type: 发送类型,告诉插件是用HTTP还是WebSocket发送消息
    # ws_client: WebSocket连接实例,ws_server: WebSocket服务端实例(若发送类型为WebSocket这两个参数必填)
    # send_host: HTTP协议发送地址,send_port: HTTP协议发送端口(若填这两个参数则使用自定义地址发送)
    threading.Thread(target=builtin_function, args=(data, send_type, ws_client, ws_server, send_host, send_port)).start()
    send_address = {}
    if send_type == "HTTP":
        send_address.update({"WebSocketClient": None, "WebSocketServer": None, "SendHost": send_host, "SendPort": send_port})
    elif send_type == "WebSocket":
        send_address.update({"WebSocketClient": ws_client, "WebSocketServer": ws_server, "SendHost": "", "SendPort": ""})
    data.update({"SendType": send_type, "SendAddress": send_address})
    for plugin in plugins_dict.values():  # 遍历开线程调用所有的插件事件函数
        try:
            threading.Thread(target=plugin.event, kwargs={"data": data}).start()
        except AttributeError:
            pass


def update_flora_api():  # 更新API内容函数
    # noinspection PyTypeChecker
    flora_api.update({"PluginsDict": plugins_dict.copy(), "PluginsInfoDict": plugins_info_dict.copy(), "HelpInfoDict": help_info_dict.copy()})
    for plugin in plugins_dict.values():
        try:
            plugin.flora_api.update(flora_api.copy())
        except AttributeError:
            pass
    for plugin in plugins_dict.values():  # 遍历开线程调用所有的API更新事件函数
        try:
            threading.Thread(target=plugin.api_update_event).start()
        except AttributeError:
            pass


def builtin_function(data: dict, send_type: str = "HTTP", ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):  # 一些内置的功能
    uid = data.get("user_id")
    gid = data.get("group_id")
    mid = data.get("message_id")
    msg = data.get("raw_message")
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        if msg == "/帮助":
            send_text = f"FloraBot {flora_version}\n\n帮助菜单:\nFloraBot 内置功能:"
            for help_class in help_info_dict.get("Flora").get("Help"):
                if help_class.get("AdminUse") is not None and help_class.get("AdminUse") and uid not in administrator:
                    continue
                send_text += f"\n  {help_class.get('Class')}:"
                for help_command in help_class.get("Commands"):
                    send_text += f"\n  •{help_command.get('Command')}  -  {help_command.get('Content')}"
            send_text += "\n\n若要查看插件的帮助菜单, 请使用指令\n\"/帮助 + [空格] + [插件名]\""
            send_msg(send_type, send_text, uid, gid, mid, ws_client, ws_server, send_host, send_port)
        elif msg.startswith("/帮助 "):
            msg = msg.replace("/帮助 ", "", 1)
            if msg in help_info_dict.get("Plugins"):
                send_text = f"FloraBot {flora_version}\n\n帮助菜单:\n{msg}:"
                for help_class in help_info_dict.get("Plugins").get(msg).get("Help"):
                    if help_class.get("AdminUse") is not None and help_class.get("AdminUse") and uid not in administrator:
                        continue
                    send_text += f"\n  {help_class.get('Class')}:"
                    for help_command in help_class.get("Commands"):
                        send_text += f"\n  •{help_command.get('Command')}  -  {help_command.get('Content')}"
                send_text += "\n\n若要查看其他插件的帮助菜单, 请使用指令\n\"/帮助 + [空格] + [插件名]\""
                send_msg(send_type, send_text, uid, gid, mid, ws_client, ws_server, send_host, send_port)
            else:
                send_msg(send_type, f"未找到插件 {msg} 的帮助", uid, gid, mid, ws_client, ws_server, send_host, send_port)
        elif msg == "/插件列表":
            plugins = f"FloraBot {flora_version}\n\n插件列表:\n"
            for plugin_info in plugins_info_dict.values():
                plugin_status = "启用"
                if not plugin_info.get("EnablePlugin"):
                    plugin_status = "禁用"
                plugins += f"•{plugin_info.get('PluginName')}  [状态: {plugin_status}]\n"
            plugins += f"\n共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件"
            if uid in administrator:
                plugins += "\n可使用 \"/启用/禁用插件 + [空格] + [插件名]\" 来启用或者禁用插件\n若未找到插件, 但插件文件已添加, 请试试使用 \"/重载插件\""
            send_msg(send_type, plugins, uid, gid, mid, ws_client, ws_server, send_host, send_port)
        elif uid in administrator:
            admin_function(msg, uid, gid, mid, send_type, ws_client, ws_server, send_host, send_port)


update_request_id = []
update_flora = False
flora_updater_py = """import shutil
import os
import subprocess
import sys

source_dir = "./FloraBot-main"
target_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

for item in os.listdir(source_dir):
    source_path = os.path.join(source_dir, item)
    target_path = os.path.join(target_dir, item)
    if os.path.exists(target_path):
        if os.path.isfile(target_path) or os.path.islink(target_path):
            os.remove(target_path)
        elif os.path.isdir(target_path):
            shutil.rmtree(target_path)
    shutil.move(source_path, target_path)
shutil.rmtree(source_dir)

subprocess.Popen([sys.executable, os.path.join(target_dir, "FloraBot.py")])
"""


def admin_function(msg: str, uid: str | int, gid: str | int | None, mid: str | int | None = None, send_type: str = "HTTP", ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):  # 一些内置的功能
    global update_flora
    if msg == "/重载插件":
        send_msg(send_type, "正在重载插件, 请稍后...", uid, gid, mid, ws_client, ws_server)
        load_plugins()
        send_msg(send_type, f"FloraBot {flora_version}\n\n插件重载完成, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid, ws_client, ws_server, send_host, send_port)
    elif msg.startswith("/启用插件 "):
        msg = msg.replace("/启用插件 ", "", 1)
        if plugins_info_dict.get(msg) is not None and not plugins_info_dict.get(msg).get("EnablePlugin"):
            plugin_info = plugins_info_dict.get(msg)
            plugin_info.update({"EnablePlugin": True})
            plugins_info_dict.update({msg: plugin_info})
            spec = importlib.util.spec_from_file_location(plugin_info.get("MainPyName"), f"./{plugin_info.get('ThePluginPath')}/{plugin_info.get('MainPyName')}.py")
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except ModuleNotFoundError as error_info:
                if auto_install:
                    install_libraries(str(error_info).split("'")[1])
                    spec.loader.exec_module(module)
                else:
                    raise ModuleNotFoundError(error_info)
            try:
                module.flora_api = flora_api.copy()
            except AttributeError:
                pass
            module.flora_api.update({"ThePluginPath": plugin_info.get("ThePluginPath")})
            try:
                threading.Thread(target=module.init).start()
            except AttributeError:
                pass
            plugins_dict.update({plugin_info.get("PluginName"): module})
            update_flora_api()
            with open(f"./{plugin_info.get('ThePluginPath')}/Plugin.json", "w", encoding="UTF-8") as write_plugin_config:
                plugin_info_copy = plugin_info.copy()
                plugin_info_copy.pop("ThePluginPath")
                write_plugin_config.write(json.dumps(plugin_info_copy, ensure_ascii=False, indent=4))
            send_msg(send_type, f"FloraBot {flora_version}\n\n插件 {msg} 已启用, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid, ws_client, ws_server, send_host, send_port)
        else:
            send_msg(send_type, f"FloraBot {flora_version}\n\n未找到或已启用插件 {msg} , 若未找到插件, 但插件文件已添加, 请试试使用 \"/重载插件\"", uid, gid, mid, ws_client, ws_server, send_host, send_port)
    elif msg.startswith("/禁用插件 "):
        msg = msg.replace("/禁用插件 ", "", 1)
        if plugins_info_dict.get(msg) is not None and plugins_info_dict.get(msg).get("EnablePlugin"):
            plugin_info = plugins_info_dict.get(msg)
            plugin_info.update({"EnablePlugin": False})
            plugins_info_dict.update({msg: plugin_info})
            if plugins_dict.get(msg) is not None:
                plugins_dict.pop(msg)
            update_flora_api()
            with open(f"./{plugin_info.get('ThePluginPath')}/Plugin.json", "w", encoding="UTF-8") as write_plugin_config:
                plugin_info_copy = plugin_info.copy()
                plugin_info_copy.pop("ThePluginPath")
                write_plugin_config.write(json.dumps(plugin_info_copy, ensure_ascii=False, indent=4))
            send_msg(send_type, f"FloraBot {flora_version}\n\n插件 {msg} 已禁用, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid, ws_client, ws_server, send_host, send_port)
        else:
            send_msg(send_type, f"FloraBot {flora_version}\n\n未找到或已禁用插件 {msg} , 若未找到插件, 但插件文件已添加, 请试试使用 \"/重载插件\"", uid, gid, mid, ws_client, ws_server, send_host, send_port)
    elif msg.startswith("/echo "):
        send_msg(send_type, msg.replace("/echo ", "", 1), uid, gid, mid, ws_client, ws_server, send_host, send_port)
    elif msg.startswith("/echo1 "):
        send_msg(send_type, msg.replace("/echo1 ", "", 1), uid, gid, None, ws_client, ws_server, send_host, send_port)
    elif msg.startswith("/API测试 "):
        search_api = re.search(r"/API测试 (.*?)( 参数|$)", msg).group(1)
        if not search_api.isspace() and search_api != "":
            search_params = re.search(r"参数 (.*)", msg)
            call_params = {}
            if search_params is not None:
                search_params = search_params.group(1)
                if not search_params.isspace() and search_params != "":
                    try:
                        call_params = json.loads(search_params)
                    except json.JSONDecodeError:
                        send_msg(send_type, "参数错误, 参数不是标准的 Json 格式", uid, gid, mid, ws_client, ws_server, send_host, send_port)
            send_msg(send_type, json.dumps(call_api(send_type, search_api, call_params, ws_client, ws_server, send_host, send_port), ensure_ascii=False, indent=4), uid, gid, mid, ws_client, ws_server,send_host, send_port)
    elif msg == "/检查更新":
        if not update_flora:
            if len(update_request_id) != 0:
                if time.time() - update_request_id[1] > 60:
                    update_request_id.clear()
                    update_flora = False
            if len(update_request_id) == 0:
                update_request_id.extend([uid, time.time()])
                send_msg(send_type, "请选择一个 GitHub 源:\n1. 官方源(github.com)\n2. gh.llkk.cc\n3. github.moeyy.xyz\n4. mirror.ghproxy.com\n5. ghproxy.net\n6. gh.ddlc.top\n\n下一步请在一分钟之内发送以下格式的指令:\n/GitHub源 + [空格] + [序号(1~6)]", uid, gid, mid, ws_client, ws_server, send_host, send_port)
            else:
                send_msg(send_type, "已经有 Bot 管理员发起了更新请求, 请稍等一会", uid, gid, mid, ws_client, ws_server, send_host, send_port)
        else:
            send_msg(send_type, "FloraBot 正在执行步骤", uid, gid, mid, ws_client, ws_server, send_host, send_port)
    elif msg.startswith("/GitHub源 ") and len(update_request_id) != 0 and not update_flora:
        if time.time() - update_request_id[1] > 60:
            update_request_id.clear()
            update_flora = False
        if len(update_request_id) != 0 and uid == update_request_id[0]:
            msg = msg.replace("/GitHub源 ", "", 1)
            try:
                update_flora = True
                file_source = "https://raw.githubusercontent.com/FloraBotTeam/FloraBot/main/FloraBot.py"
                download_source = ""
                msg = int(msg)
                if msg == 1:
                    send_msg(send_type, "你选择了 1, 即将使用 官方 源", uid, gid, mid, ws_client, ws_server, send_host, send_port)
                elif msg == 2:
                    download_source = "https://gh.llkk.cc/"
                    send_msg(send_type, "你选择了 2, 即将使用 gh.llkk.cc 镜像源", uid, gid, mid, ws_client, ws_server, send_host, send_port)
                elif msg == 3:
                    download_source = "https://github.moeyy.xyz/"
                    send_msg(send_type, "你选择了 3, 即将使用 github.moeyy.xyz 镜像源", uid, gid, mid, ws_client, ws_server, send_host, send_port)
                elif msg == 4:
                    download_source = "https://mirror.ghproxy.com/"
                    send_msg(send_type, "你选择了 4, 即将使用 mirror.ghproxy.com 镜像源", uid, gid, mid, ws_client, ws_server, send_host, send_port)
                elif msg == 5:
                    download_source = "https://ghproxy.net/"
                    send_msg(send_type, "你选择了 5, 即将使用 ghproxy.net 镜像源", uid, gid, mid, ws_client, ws_server, send_host, send_port)
                elif msg == 6:
                    download_source = "https://gh.ddlc.top/"
                    send_msg(send_type, "你选择了 6, 即将使用 gh.ddlc.top 镜像源", uid, gid, mid, ws_client, ws_server, send_host, send_port)
                else:
                    update_flora = False
                    send_msg(send_type, "参数错误, 序号的范围应该为 1~6\n正确的指令格式为:\n/GitHub源 + [空格] + [序号(1~6)]", uid, gid, mid, ws_client, ws_server, send_host, send_port)
                if 1 <= msg <= 6:
                    send_msg(send_type, "开始检查更新 FloraBot, 请稍后...", uid, gid, None, ws_client, ws_server, send_host, send_port)
                    try:
                        update_request_id.append(download_source)
                        response = requests.get(download_source + file_source)
                        response.raise_for_status()
                        get_version = re.search(r'flora_version\s*=\s*"(.+?)"', response.text)
                        if get_version is not None:
                            get_version = get_version.group(1)
                            if get_version != flora_version:
                                get_update_content = re.search(r'update_content\s*=\s*"""(.+?)"""', response.text)
                                if get_update_content is not None:
                                	get_update_content = get_update_content.group(1)
                                else:
                                	get_update_content = "None"
                                send_msg(send_type, f"检查到 FloraBot 有新的版本, 当前版本为 {flora_version}, 最新版本为 {get_version}, 更新内容:\n{get_update_content}", uid, gid, None, ws_client, ws_server, send_host, send_port)
                                is_big_update = re.search(r"\bbig_update\s*=\s*True\b", response.text)
                                send_text = ""
                                if is_big_update is not None:
                                    send_text = "更新到最新版本为大更新, 可能会出现插件功能失效等问题\n\n"
                                send_text += "确认要更新到最新版吗?\n\n下一步请在一分钟之内发送以下指令:\n/确认更新"
                                update_request_id[1] = time.time()
                                send_msg(send_type, send_text, uid, gid, mid, ws_client, ws_server, send_host, send_port)
                            else:
                                update_flora = False
                                send_msg(send_type, f"FloraBot 当前已是最新版本", uid, gid, None, ws_client, ws_server, send_host, send_port)
                        else:
                            update_flora = False
                            send_msg(send_type, f"FloraBot 检查更新失败, 获取版本号失败", uid, gid, None, ws_client, ws_server, send_host, send_port)
                    except requests.RequestException as error_info:
                        update_flora = False
                        send_msg(send_type, f"FloraBot 检查更新失败, 网络请求出现异常, 详细信息: {error_info}", uid, gid, None, ws_client, ws_server, send_host, send_port)
            except ValueError:
                update_flora = False
                send_msg(send_type, "参数错误, 这好像不是序号吧\n正确的指令格式为:\n/GitHub源 + [空格] + [序号(1~6)]", uid, gid, mid, ws_client, ws_server, send_host, send_port)
    elif msg == "/确认更新" and len(update_request_id) != 0 and update_flora:
        if time.time() - update_request_id[1] > 60:
            update_request_id.clear()
            update_flora = False
        if len(update_request_id) != 0 and uid == update_request_id[0]:
            send_msg(send_type, "开始更新 FloraBot, 请稍后...", uid, gid, mid, ws_client, ws_server, send_host, send_port)
            try:
                send_msg(send_type, "开始下载 FloraBot ...", uid, gid, None, ws_client, ws_server, send_host, send_port)
                response = requests.get(update_request_id[2] + "https://github.com/FloraBotTeam/FloraBot/archive/main.zip")
                response.raise_for_status()
                if not os.path.isdir("./FloraBot/UpdateCache"):
                    os.makedirs("./FloraBot/UpdateCache")
                with open("./FloraBot/UpdateCache/FloraBot.zip", "wb") as flora_file:
                    flora_file.write(response.content)
                send_msg(send_type, "FloraBot 下载完成, 开始解压 FloraBot ...", uid, gid, None, ws_client, ws_server, send_host, send_port)
                zip_object = zipfile.ZipFile("./FloraBot/UpdateCache/FloraBot.zip")
                for file in zip_object.namelist():
                    zip_object.extract(file, "./FloraBot/UpdateCache")
                zip_object.close()
                send_msg(send_type, "FloraBot 解压完成, 开始更新依赖的库...", uid, gid, None, ws_client, ws_server, send_host, send_port)
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "./FloraBot/UpdateCache/FloraBot-main/requirements.txt"])
                    send_msg(send_type, "依赖的库更新完成, 开始替换更新 FloraBot, 这将会重启 FloraBot, FloraBot 重启后即为更新完成", uid, gid, None, ws_client, ws_server, send_host, send_port)
                except subprocess.CalledProcessError:
                    send_msg(send_type, "依赖的库更新失败, 跳过更新依赖的库, 开始替换更新 FloraBot, 这将会重启 FloraBot, FloraBot 重启后即为更新完成", uid, gid, None, ws_client, ws_server, send_host, send_port)
                with open("./FloraBot/UpdateCache/FloraUpdater.py", "w") as flora_updater:
                    flora_updater.write(flora_updater_py)
                subprocess.Popen([sys.executable, "./FloraBot/UpdateCache/FloraUpdater.py"])
                # noinspection PyUnresolvedReferences
                # noinspection PyProtectedMember
                os._exit(0)
            except requests.RequestException as error_info:
                update_flora = False
                send_msg(send_type, f"FloraBot 更新失败, 网络请求出现异常, 详细信息: {error_info}", uid, gid, None, ws_client, ws_server, send_host, send_port)


@flora_server.post("/")
def http_message_received():  # HTTP协议消息接收函数,不要主动调用这个函数
    data = request.get_json()  # 获取提交数据
    threading.Thread(target=broadcast_event, args=(data, "HTTP"))  # 遍历开线程调用所有的插件事件函数
    return "OK"


call_api_return = []  # WebSocket协议等待回调编号注册列表(按先后顺序)
call_api_returned = {}  # WebSocket协议等待回调结果字典, 键值为: {编号: 数据}


def ws_message_received(client, server, message):  # WebSocket消息接收函数,不要主动调用这个函数
    global call_api_return, call_api_returned
    try:
        data = json.loads(message)
        if "status" in data and len(call_api_return) != 0:
            call_api_returned.update({call_api_return.pop(0): data})
        elif data.get("meta_event_type") != "heartbeat":
            threading.Thread(target=broadcast_event, args=(data, "WebSocket", client, server)).start()  # 遍历开线程调用所有的插件事件函数
    except json.JSONDecodeError:
        pass


def check_privileges():
    system = platform.system()
    print(f"当前系统为 {system}")
    if system == "Windows":
        try:
            from ctypes import windll
            is_admin = windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False
        if is_admin:
            print("\033[91m警告: 当前用户具有管理员权限, 若是添加了恶意插件, 后果不堪设想!!!\033[0m")
    elif system in ["Linux", "Darwin"]:
        if os.geteuid() == 0:
            print("\033[91m警告: 当前用户具有 root 权限, 若是添加了恶意插件, 后果不堪设想!!!\033[0m")


logger = logging.getLogger(__name__)
logging.basicConfig()


class FloraWebSocketHandler(WebSocketHandler):  # 重写WebSocketHandler类
    def read_http_headers(self):
        headers = {}
        http_get = self.rfile.readline().decode().strip()
        if not http_get.upper().startswith("GET"):
            logger.warning("框架使用了不正确的 HTTP 方法进行请求 WebSocket 通信")
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
            with self._send_lock:
                self.request.sendall(response.encode())
            self.keep_alive = False
            return headers
        while True:
            header = self.rfile.readline().decode().strip()
            if not header:
                break
            head, value = header.split(":", 1)
            headers[head.lower().strip()] = value.strip()
        return headers

    def handshake(self):
        headers = self.read_http_headers()
        if "upgrade" in headers:
            try:
                assert headers["upgrade"].lower() == "websocket"
            except AssertionError:
                self.keep_alive = False
                return
            try:
                key = headers["sec-websocket-key"]
            except KeyError:
                logger.warning("框架尝试进行连接, 但缺少密钥")
                self.keep_alive = False
                return
            response = self.make_handshake_response(key)
            with self._send_lock:
                self.handshake_done = self.request.send(response.encode())
            self.valid_client = True
            self.server._new_client_(self)
        else:
            logger.warning("框架使用了不正确的 WebSocket 协议进行通信")
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"
            with self._send_lock:
                self.request.sendall(response.encode())
            self.keep_alive = False


class FloraWebsocketServer(WebsocketServer):  # 重写WebsocketServer类
    def __init__(self, host="127.0.0.1", port=0, loglevel=logging.WARNING, key=None, cert=None):
        logger.setLevel(loglevel)
        # noinspection PyTypeChecker
        TCPServer.__init__(self, (host, port), FloraWebSocketHandler)
        self.host = host
        self.port = self.socket.getsockname()[1]
        self.key = key
        self.cert = cert
        self.clients = []
        self.id_counter = 0
        self.thread = None
        self._deny_clients = False


def client_connect(client, server):
    global exit_flag
    exit_flag = False
    print(f"框架已通过 WebSocket 连接, 连接ID: {client.get('id')}")


exit_flag = False


def client_left(client, server):
    global call_api_return, call_api_returned, exit_flag
    if client is not None:
        exit_flag = True
        call_api_return.clear()
        call_api_returned.clear()
        print(f"框架已从 WebSocket 连接断开, 连接ID: {client.get('id')}")


flora_api = {"FloraPath": os.path.dirname(os.path.abspath(__file__)), "ConnectionType": connection_type, "FloraHost": flora_host, "FloraPort": flora_port, "FrameworkAddress": framework_address, "BotID": bot_id, "Administrator": administrator, "FloraVersion": flora_version, "FloraServer": flora_server, "CallApiReturned": call_api_returned, "UpdateFloraApi": update_flora_api, "LoadPlugins": load_plugins, "BroadcastEvent": broadcast_event, "SendMsg": send_msg, "CallApi": call_api}


if __name__ == "__main__":
    print(flora_logo)
    check_privileges()
    print("正在初始化 FloraBot , 请稍后...")
    load_config()
    print(f"欢迎使用 FloraBot {flora_version}")
    print("\033[93m声明: 插件为第三方内容, 请您自行分辨是否为恶意插件, 若被恶意插件入侵/破坏了您的设备或恶意盗取了您的信息, 造成的损失请自负, FloraBotTeam 概不负责也无义务负责!!!\033[0m")
    load_plugins()
    print(f"框架连接方式为: {connection_type}")
    if connection_type == "HTTP":
        flora_server.run(host=flora_host, port=flora_port)
    elif connection_type == "WebSocket":
        flora_server_ws = FloraWebsocketServer(host=flora_host, port=flora_port)
        flora_server_ws.set_fn_new_client(client_connect)
        flora_server_ws.set_fn_client_left(client_left)
        flora_server_ws.set_fn_message_received(ws_message_received)
        flora_server_ws.run_forever()
