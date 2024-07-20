from flask import Flask, request
import requests
import importlib.util
import os
import json
import threading

flora_logo = """
███████╗ ██╗                          ██████╗
██╔════╝ ██║                          ██╔══██╗           ██╗
█████╗   ██║   ████╗   ████╗  ████╗   ██████╔╝  ████╗  ██████╗
██╔══╝   ██║  ██╔═██╗ ██╔══╝ ██╔═██╗  ██╔══██╗ ██╔═██╗  ╚██╔═╝
██║      ███╗ ╚████╔╝ ██║    ╚██████╗ ██████╔╝ ╚████╔╝   ███╗
╚═╝      ╚══╝  ╚═══╝  ╚═╝     ╚═════╝ ╚═════╝   ╚═══╝    ╚══╝
"""
flora_server = Flask("FloraBot", template_folder="FloraBot", static_folder="FloraBot")
flora_host = "127.0.0.1"
flora_port = 3003
framework_address = "127.0.0.1:3000"
administrator = 0

flora_version = "v1.0"
plugins_dict = {}  # 插件对象字典
plugins_info_dict = {}  # 插件信息字典


def load_config():  # 加载FloraBot配置文件函数
    global flora_host, flora_port, framework_address, administrator
    if os.path.isfile("./Config.json"):  # 若文件存在
        with open("./Config.json", "r", encoding="UTF-8") as read_flora_config:
            flora_config = json.loads(read_flora_config.read())
        flora_host = flora_config.get("FloraHost")
        flora_port = flora_config.get("FloraPort")
        framework_address = flora_config.get("FrameworkAddress")
        administrator = flora_config.get("Administrator")
        flora_api.update({"Administrator": administrator})
    else:  # 若文件不存在
        print("FloraBot 启动失败, 未找到配置文件 Config.json")
        with open("./Config.json", "w", encoding="UTF-8") as write_flora_config:
            write_flora_config.write(json.dumps({"FloraHost": "127.0.0.1", "FloraPort": 3003, "FrameworkAddress": "127.0.0.1:3000", "Administrator": 0, "NameList": False}, ensure_ascii=False, indent=4))
        print("已生成一个新的配置文件 Config.json , 请修改后再次启动 FloraBot")
        exit()


def send_msg(msg: str, uid: str | int, gid: str | int | None, mid: str | int = None):  # 发送信息函数,msg: 正文,uid: QQ号,gid: 群号,mid: 消息编号
    url = f"http://{framework_address}"
    data = {}
    if mid is not None:  # 当消息编号不为None时,则发送的消息为回复
        data.update({"message": f"[CQ:reply,id={mid}]{msg}"})
    else:  # 反之为普通消息
        data.update({"message": msg})
    if gid is not None:  # 当群号不为None时,则发送给群聊
        url = f"{url}/send_group_msg"
        data.update({"group_id": gid})
    else:  # 反之为私聊
        url = f"{url}/send_private_msg"
        data.update({"user_id": uid})
    try:
        requests.post(url, data=data, timeout=5)  # 提交发送消息
    except requests.exceptions.RequestException:
        pass


def load_plugins():  # 加载插件函数
    print("正在加载插件, 请稍后...\n")
    plugins_info_dict.clear()
    plugins_dict.clear()
    for plugin in os.listdir("./FloraBot/Plugins"):  # 遍历所有插件
        plugin_path = f"./FloraBot/Plugins/{plugin}"
        if os.path.isfile(f"{plugin_path}/Plugin.json"):
            with open(f"{plugin_path}/Plugin.json", "r", encoding="UTF-8") as read_plugin_config:
                plugin_config = json.loads(read_plugin_config.read())
            if os.path.isfile(f"{plugin_path}/{plugin_config.get('MainPyName')}.py") and plugin_config.get("EnablePlugin"):  # 如果配置正确则导入插件
                plugin_config = plugin_config.copy()
                plugin_config.update({"ThePluginPath": plugin_path})
                plugins_info_dict.update({plugin_config.get("PluginName"): plugin_config})  # 添加插件信息
                spec = importlib.util.spec_from_file_location(plugin_config.get("MainPyName"), f"./FloraBot/Plugins/{plugin}/{plugin_config.get('MainPyName')}.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.flora_api = flora_api.copy()  # 传入API参数
                module.flora_api.update({"ThePluginPath": plugin_path})
                threading.Thread(target=module.init).start()  # 开线程初始化插件
                plugins_dict.update({plugin_config.get("PluginName"): module})  # 添加插件对象
    update_flora_api()


def update_flora_api():  # 更新API内容函数
    # noinspection PyTypeChecker
    flora_api.update({"PluginsDict": plugins_dict.copy(), "PluginsInfoDict": plugins_info_dict.copy()})
    for plugin in plugins_dict.values():
        plugin.flora_api.update(flora_api.copy())


flora_api = {"FloraHost": flora_host, "FloraPort": flora_port, "FrameworkAddress": framework_address, "FloraVersion": flora_version, "FloraServer": flora_server, "UpdateFloraApi": update_flora_api, "LoadPlugins": load_plugins, "SendMsg": send_msg}


@flora_server.post("/")
def process():  # 消息处理函数,不要主动调用这个函数
    data = request.get_json()  # 获取提交数据
    uid = data.get('user_id')
    if uid == administrator:  # 判断消息是否来自于管理员(主人)
        gid = data.get('group_id')
        mid = data.get('message_id')
        msg = data.get('raw_message').replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        if msg == "重载插件":
            send_msg("正在重载插件, 请稍后...", uid, gid, mid)
            load_plugins()
            send_msg(f"FloraBot {flora_version}\n\n插件重载完成, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid)
        elif msg == "插件列表":
            plugins = f"FloraBot {flora_version}\n\n插件列表:\n"
            for plugin_info in plugins_info_dict.values():
                plugin_status = "启用"
                if not plugin_info.get("EnablePlugin"):
                    plugin_status = "禁用"
                plugins += f"•{plugin_info.get('PluginName')}  [状态: {plugin_status}]\n"
            plugins += f"\n共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件\n可使用 \"启用/禁用插件 + [插件名]\" 来启用或者禁用插件\n若未找到插件, 但插件文件已添加, 请试试使用 \"重载插件\""
            send_msg(plugins, uid, gid, mid)
        elif msg.startswith("启用插件 "):
            msg = msg.replace("启用插件 ", "")
            if plugins_info_dict.get(msg) is not None and not plugins_info_dict.get(msg).get("EnablePlugin"):
                plugin_info = plugins_info_dict.get(msg)
                plugin_info.update({"EnablePlugin": True})
                plugins_info_dict.update({msg: plugin_info})
                spec = importlib.util.spec_from_file_location(plugin_info.get("MainPyName"), f"{plugin_info.get('ThePluginPath')}/{plugin_info.get('MainPyName')}.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.flora_api = flora_api.copy()
                module.flora_api.update({"ThePluginPath": plugin_info.get("ThePluginPath")})
                threading.Thread(target=module.init).start()
                plugins_dict.update({plugin_info.get("PluginName"): module})
                update_flora_api()
                with open(f"{plugin_info.get('ThePluginPath')}/Plugin.json", "w", encoding="UTF-8") as write_plugin_config:
                    plugin_info_copy = plugin_info.copy()
                    plugin_info_copy.pop("ThePluginPath")
                    write_plugin_config.write(json.dumps(plugin_info_copy, ensure_ascii=False, indent=4))
                send_msg(f"FloraBot {flora_version}\n\n插件 {msg} 已启用, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid)
            else:
                send_msg(f"FloraBot {flora_version}\n\n未找到或已启用插件 {msg} , 若未找到插件, 但插件文件已添加, 请试试使用 \"重载插件\"", uid, gid, mid)
        elif msg.startswith("禁用插件 "):
            msg = msg.replace("禁用插件 ", "")
            if plugins_info_dict.get(msg) is not None and plugins_info_dict.get(msg).get("EnablePlugin"):
                plugin_info = plugins_info_dict.get(msg)
                plugin_info.update({"EnablePlugin": False})
                plugins_info_dict.update({msg: plugin_info})
                if plugins_dict.get(msg) is not None:
                    plugins_dict.pop(msg)
                update_flora_api()
                with open(f"{plugin_info.get('ThePluginPath')}/Plugin.json", "w", encoding="UTF-8") as write_plugin_config:
                    plugin_info_copy = plugin_info.copy()
                    plugin_info_copy.pop("ThePluginPath")
                    write_plugin_config.write(json.dumps(plugin_info_copy, ensure_ascii=False, indent=4))
                send_msg(f"FloraBot {flora_version}\n\n插件 {msg} 已禁用, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid)
            else:
                send_msg(f"FloraBot {flora_version}\n\n未找到或已禁用插件 {msg} , 若未找到插件, 但插件文件已添加, 请试试使用 \"重载插件\"", uid, gid, mid)
    for plugin in plugins_dict.values():  # 遍历开线程调用所有的插件事件函数
        threading.Thread(target=plugin.event, args=(data,)).start()
    return "OK"


if __name__ == "__main__":
    print(flora_logo)
    print("正在初始化 FloraBot , 请稍后...")
    if not os.path.isdir("./FloraBot"):
        os.makedirs("./FloraBot")
    if not os.path.isdir("./FloraBot/Plugins"):
        os.makedirs("./FloraBot/Plugins")
    load_config()
    print(f"欢迎使用 FloraBot {flora_version}\n")
    load_plugins()
    flora_server.run(host=flora_host, port=flora_port)
