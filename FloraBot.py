from flask import Flask, request
import requests
import importlib.util
import os
import json
import threading

flora_server = Flask("FloraBot", template_folder="FloraBot", static_folder="FloraBot")
flora_host = "127.0.0.1"
flora_port = 3003
framework_address = "127.0.0.1:3000"
administrator = 0

flora_version = "1.0"
plugins_dict = {}
plugins_info_dict = {}


def load_config():
    global flora_host, flora_port, framework_address, administrator
    if os.path.isfile("./Config.json"):
        with open("./Config.json", "r", encoding="UTF-8") as read_flora_config:
            flora_config = json.loads(read_flora_config.read())
        flora_host = flora_config.get("FloraHost")
        flora_port = flora_config.get("FloraPort")
        framework_address = flora_config.get("FrameworkAddress")
        administrator = flora_config.get("Administrator")
    else:
        print("FloraBot 启动失败, 未找到配置文件 Config.json")
        with open("./Config.json", "w", encoding="UTF-8") as write_flora_config:
            write_flora_config.write(json.dumps({"FloraHost": "127.0.0.1", "FloraPort": 3003, "FrameworkAddress": "127.0.0.1:3000", "Administrator": 0, "NameList": False}, ensure_ascii=False, indent=4))
        print("已生成一个新的配置文件 Config.json , 请修改后再次启动 FloraBot")
        exit()


def send_msg(msg: str, uid: str | int, gid: str | int | None, mid: str | int = None):
    url = f"http://{framework_address}"
    data = {}
    if mid is not None:
        data.update({"message": f"[CQ:reply,id={mid}]{msg}"})
    else:
        data.update({"message": msg})
    if gid is not None:
        url += "/send_group_msg"
        data.update({"group_id": gid})
    else:
        url += "/send_private_msg"
        data.update({"user_id": uid})
    try:
        requests.post(url, data=data, timeout=5)
    except requests.exceptions.RequestException:
        pass


def load_plugins():
    plugins_info_dict.clear()
    for plugin in os.listdir("./FloraBot/Plugins"):
        plugin_path = f"./FloraBot/Plugins/{plugin}"
        if os.path.isfile(f"{plugin_path}/Plugin.json"):
            with open(f"{plugin_path}/Plugin.json", "r", encoding="UTF-8") as read_plugin_config:
                plugin_config = json.loads(read_plugin_config.read())
            plugin_config.update({"ThePluginPath": plugin_path})
            plugins_info_dict.update({plugin_config.get("PluginName"): plugin_config})
    plugins_dict.clear()
    flora_api = {}
    flora_api.update(globals())
    for plugin in os.listdir("./FloraBot/Plugins"):
        plugin_path = f"./FloraBot/Plugins/{plugin}"
        if os.path.isfile(f"{plugin_path}/Plugin.json"):
            with open(f"{plugin_path}/Plugin.json", "r", encoding="UTF-8") as read_plugin_config:
                plugin_config = json.loads(read_plugin_config.read())
            if os.path.isfile(f"{plugin_path}/{plugin_config.get('MainPyName')}.py") and plugin_config.get("EnablePlugin"):
                flora_api.update({"ThePluginPath": plugin_path})
                spec = importlib.util.spec_from_file_location(plugin_config.get("MainPyName"), f"./FloraBot/Plugins/{plugin}/{plugin_config.get('MainPyName')}.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.flora_api = flora_api
                threading.Thread(target=module.init).start()
                plugins_dict.update({plugin_config.get("PluginName"): module})


def update_flora_api():
    for plugin in plugins_dict.values():
        plugin.flora_api.update(globals())


@flora_server.post("/")
def process():
    data = request.get_json()
    uid = data.get('user_id')
    gid = data.get('group_id')
    mid = data.get('message_id')
    msg = data.get('raw_message').replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")
    if uid == administrator:
        if msg == "重载插件":
            load_plugins()
            send_msg(f"FloraBot v{flora_version}\n\n插件重载完成, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid)
        elif msg == "插件列表":
            plugins = "FloraBot v{flora_version}\n\n插件列表:\n"
            for plugin_info in plugins_info_dict.values():
                plugin_status = "启用"
                if not plugin_info.get("EnablePlugin"):
                    plugin_status = "禁用"
                plugins += f"•{plugin_info.get('PluginName')}  [状态: {plugin_status}]\n"
            plugins += f"\n共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件\n可使用 \"启用/禁用插件 + 插件名\" 来启用或者禁用插件\n若未找到插件, 但插件文件已添加, 请试试使用 \"重载插件\""
            send_msg(plugins, uid, gid, mid)
        elif msg.startswith("启用插件 "):
            msg = msg.replace("启用插件 ", "")
            flora_api = {}
            flora_api.update(globals())
            if plugins_info_dict.get(msg) is not None and not plugins_info_dict.get(msg).get("EnablePlugin"):
                plugin_info = plugins_info_dict.get(msg)
                plugin_info.update({"EnablePlugin": True})
                plugins_info_dict.update({msg: plugin_info})
                flora_api.update({"ThePluginPath": plugin_info.get("ThePluginPath")})
                spec = importlib.util.spec_from_file_location(plugin_info.get("MainPyName"), f"{plugin_info.get('ThePluginPath')}/{plugin_info.get('MainPyName')}.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                module.flora_api = flora_api
                threading.Thread(target=module.init).start()
                plugins_dict.update({plugin_info.get("PluginName"): module})
                update_flora_api()
                with open(f"{plugin_info.get('ThePluginPath')}/Plugin.json", "w", encoding="UTF-8") as write_plugin_config:
                    plugin_info_copy = plugin_info.copy()
                    plugin_info_copy.pop("ThePluginPath")
                    write_plugin_config.write(json.dumps(plugin_info_copy, ensure_ascii=False, indent=4))
                send_msg(f"FloraBot v{flora_version}\n\n插件 {msg} 已启用, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid)
            else:
                send_msg(f"FloraBot v{flora_version}\n\n未找到或已启用插件 {msg} , 若未找到插件, 但插件文件已添加, 请试试使用 \"重载插件\"", uid, gid, mid)
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
                send_msg(f"FloraBot v{flora_version}\n\n插件 {msg} 已禁用, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid)
            else:
                send_msg(f"FloraBot v{flora_version}\n\n未找到或已禁用插件 {msg} , 若未找到插件, 但插件文件已添加, 请试试使用 \"重载插件\"", uid, gid, mid)
    for plugin in plugins_dict.values():
        threading.Thread(target=plugin.event, args=(data,)).start()
    return "OK"


if __name__ == "__main__":
    if not os.path.isdir("./FloraBot"):
        os.makedirs("./FloraBot")
    if not os.path.isdir("./FloraBot/Plugins"):
        os.makedirs("./FloraBot/Plugins")
    load_config()
    load_plugins()
    flora_server.run(host=flora_host, port=flora_port)

