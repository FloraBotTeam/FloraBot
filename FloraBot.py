from flask import Flask, request
import requests
import importlib.util
import os
import json
import threading
import sys
import subprocess
import platform
import ctypes

flora_logo = "\x1b[38;2;255;0;0m█\x1b[38;2;250;0;4m█\x1b[38;2;246;0;8m█\x1b[38;2;242;0;12m█\x1b[38;2;238;0;16m█\x1b[38;2;234;0;20m█\x1b[38;2;229;0;25m█\x1b[38;2;225;0;29m╗\x1b[38;2;221;0;33m \x1b[38;2;217;0;37m█\x1b[38;2;213;0;41m█\x1b[38;2;209;0;45m╗\x1b[38;2;204;0;50m \x1b[38;2;200;0;54m \x1b[38;2;196;0;58m \x1b[38;2;192;0;62m \x1b[38;2;188;0;66m \x1b[38;2;183;0;71m \x1b[38;2;179;0;75m \x1b[38;2;175;0;79m \x1b[38;2;171;0;83m \x1b[38;2;167;0;87m \x1b[38;2;163;0;91m \x1b[38;2;158;0;96m \x1b[38;2;154;0;100m \x1b[38;2;150;0;104m \x1b[38;2;146;0;108m \x1b[38;2;142;0;112m \x1b[38;2;137;0;117m \x1b[38;2;133;0;121m \x1b[38;2;129;0;125m \x1b[38;2;125;0;129m \x1b[38;2;121;0;133m \x1b[38;2;117;0;137m \x1b[38;2;112;0;142m \x1b[38;2;108;0;146m \x1b[38;2;104;0;150m \x1b[38;2;100;0;154m \x1b[38;2;96;0;158m█\x1b[38;2;91;0;163m█\x1b[38;2;87;0;167m█\x1b[38;2;83;0;171m█\x1b[38;2;79;0;175m█\x1b[38;2;75;0;179m█\x1b[38;2;71;0;183m╗\x1b[38;2;66;0;188m \x1b[38;2;62;0;192m \x1b[38;2;58;0;196m \x1b[38;2;54;0;200m \x1b[38;2;50;0;204m \x1b[38;2;45;0;209m \x1b[38;2;41;0;213m \x1b[38;2;37;0;217m \x1b[38;2;33;0;221m \x1b[38;2;29;0;225m \x1b[38;2;25;0;229m \x1b[38;2;20;0;234m \x1b[38;2;16;0;238m \x1b[38;2;12;0;242m \x1b[38;2;8;0;246m \x1b[38;2;4;0;250m \x1b[38;2;0;0;255m \x1b[0m\n\x1b[38;2;255;0;0m█\x1b[38;2;250;0;4m█\x1b[38;2;246;0;8m╔\x1b[38;2;242;0;12m═\x1b[38;2;238;0;16m═\x1b[38;2;234;0;20m═\x1b[38;2;229;0;25m═\x1b[38;2;225;0;29m╝\x1b[38;2;221;0;33m \x1b[38;2;217;0;37m█\x1b[38;2;213;0;41m█\x1b[38;2;209;0;45m║\x1b[38;2;204;0;50m \x1b[38;2;200;0;54m \x1b[38;2;196;0;58m \x1b[38;2;192;0;62m \x1b[38;2;188;0;66m \x1b[38;2;183;0;71m \x1b[38;2;179;0;75m \x1b[38;2;175;0;79m \x1b[38;2;171;0;83m \x1b[38;2;167;0;87m \x1b[38;2;163;0;91m \x1b[38;2;158;0;96m \x1b[38;2;154;0;100m \x1b[38;2;150;0;104m \x1b[38;2;146;0;108m \x1b[38;2;142;0;112m \x1b[38;2;137;0;117m \x1b[38;2;133;0;121m \x1b[38;2;129;0;125m \x1b[38;2;125;0;129m \x1b[38;2;121;0;133m \x1b[38;2;117;0;137m \x1b[38;2;112;0;142m \x1b[38;2;108;0;146m \x1b[38;2;104;0;150m \x1b[38;2;100;0;154m \x1b[38;2;96;0;158m█\x1b[38;2;91;0;163m█\x1b[38;2;87;0;167m╔\x1b[38;2;83;0;171m═\x1b[38;2;79;0;175m═\x1b[38;2;75;0;179m█\x1b[38;2;71;0;183m█\x1b[38;2;66;0;188m╗\x1b[38;2;62;0;192m \x1b[38;2;58;0;196m \x1b[38;2;54;0;200m \x1b[38;2;50;0;204m \x1b[38;2;45;0;209m \x1b[38;2;41;0;213m \x1b[38;2;37;0;217m \x1b[38;2;33;0;221m \x1b[38;2;29;0;225m \x1b[38;2;25;0;229m \x1b[38;2;20;0;234m \x1b[38;2;16;0;238m█\x1b[38;2;12;0;242m█\x1b[38;2;8;0;246m╗\x1b[38;2;4;0;250m \x1b[38;2;0;0;255m \x1b[0m\n\x1b[38;2;255;0;0m█\x1b[38;2;250;0;4m█\x1b[38;2;246;0;8m█\x1b[38;2;242;0;12m█\x1b[38;2;238;0;16m█\x1b[38;2;234;0;20m╗\x1b[38;2;229;0;25m \x1b[38;2;225;0;29m \x1b[38;2;221;0;33m \x1b[38;2;217;0;37m█\x1b[38;2;213;0;41m█\x1b[38;2;209;0;45m║\x1b[38;2;204;0;50m \x1b[38;2;200;0;54m \x1b[38;2;196;0;58m \x1b[38;2;192;0;62m█\x1b[38;2;188;0;66m█\x1b[38;2;183;0;71m█\x1b[38;2;179;0;75m█\x1b[38;2;175;0;79m╗\x1b[38;2;171;0;83m \x1b[38;2;167;0;87m \x1b[38;2;163;0;91m \x1b[38;2;158;0;96m█\x1b[38;2;154;0;100m█\x1b[38;2;150;0;104m█\x1b[38;2;146;0;108m█\x1b[38;2;142;0;112m╗\x1b[38;2;137;0;117m \x1b[38;2;133;0;121m \x1b[38;2;129;0;125m█\x1b[38;2;125;0;129m█\x1b[38;2;121;0;133m█\x1b[38;2;117;0;137m█\x1b[38;2;112;0;142m╗\x1b[38;2;108;0;146m \x1b[38;2;104;0;150m \x1b[38;2;100;0;154m \x1b[38;2;96;0;158m█\x1b[38;2;91;0;163m█\x1b[38;2;87;0;167m█\x1b[38;2;83;0;171m█\x1b[38;2;79;0;175m█\x1b[38;2;75;0;179m█\x1b[38;2;71;0;183m╔\x1b[38;2;66;0;188m╝\x1b[38;2;62;0;192m \x1b[38;2;58;0;196m \x1b[38;2;54;0;200m█\x1b[38;2;50;0;204m█\x1b[38;2;45;0;209m█\x1b[38;2;41;0;213m█\x1b[38;2;37;0;217m╗\x1b[38;2;33;0;221m \x1b[38;2;29;0;225m \x1b[38;2;25;0;229m█\x1b[38;2;20;0;234m█\x1b[38;2;16;0;238m█\x1b[38;2;12;0;242m█\x1b[38;2;8;0;246m█\x1b[38;2;4;0;250m█\x1b[38;2;0;0;255m╗\x1b[0m\n\x1b[38;2;255;0;0m█\x1b[38;2;250;0;4m█\x1b[38;2;246;0;8m╔\x1b[38;2;242;0;12m═\x1b[38;2;238;0;16m═\x1b[38;2;234;0;20m╝\x1b[38;2;229;0;25m \x1b[38;2;225;0;29m \x1b[38;2;221;0;33m \x1b[38;2;217;0;37m█\x1b[38;2;213;0;41m█\x1b[38;2;209;0;45m║\x1b[38;2;204;0;50m \x1b[38;2;200;0;54m \x1b[38;2;196;0;58m█\x1b[38;2;192;0;62m█\x1b[38;2;188;0;66m╔\x1b[38;2;183;0;71m═\x1b[38;2;179;0;75m█\x1b[38;2;175;0;79m█\x1b[38;2;171;0;83m╗\x1b[38;2;167;0;87m \x1b[38;2;163;0;91m█\x1b[38;2;158;0;96m█\x1b[38;2;154;0;100m╔\x1b[38;2;150;0;104m═\x1b[38;2;146;0;108m═\x1b[38;2;142;0;112m╝\x1b[38;2;137;0;117m \x1b[38;2;133;0;121m█\x1b[38;2;129;0;125m█\x1b[38;2;125;0;129m╔\x1b[38;2;121;0;133m═\x1b[38;2;117;0;137m█\x1b[38;2;112;0;142m█\x1b[38;2;108;0;146m╗\x1b[38;2;104;0;150m \x1b[38;2;100;0;154m \x1b[38;2;96;0;158m█\x1b[38;2;91;0;163m█\x1b[38;2;87;0;167m╔\x1b[38;2;83;0;171m═\x1b[38;2;79;0;175m═\x1b[38;2;75;0;179m█\x1b[38;2;71;0;183m█\x1b[38;2;66;0;188m╗\x1b[38;2;62;0;192m \x1b[38;2;58;0;196m█\x1b[38;2;54;0;200m█\x1b[38;2;50;0;204m╔\x1b[38;2;45;0;209m═\x1b[38;2;41;0;213m█\x1b[38;2;37;0;217m█\x1b[38;2;33;0;221m╗\x1b[38;2;29;0;225m \x1b[38;2;25;0;229m \x1b[38;2;20;0;234m╚\x1b[38;2;16;0;238m█\x1b[38;2;12;0;242m█\x1b[38;2;8;0;246m╔\x1b[38;2;4;0;250m═\x1b[38;2;0;0;255m╝\x1b[0m\n\x1b[38;2;255;0;0m█\x1b[38;2;250;0;4m█\x1b[38;2;246;0;8m║\x1b[38;2;242;0;12m \x1b[38;2;238;0;16m \x1b[38;2;234;0;20m \x1b[38;2;229;0;25m \x1b[38;2;225;0;29m \x1b[38;2;221;0;33m \x1b[38;2;217;0;37m█\x1b[38;2;213;0;41m█\x1b[38;2;209;0;45m█\x1b[38;2;204;0;50m╗\x1b[38;2;200;0;54m \x1b[38;2;196;0;58m╚\x1b[38;2;192;0;62m█\x1b[38;2;188;0;66m█\x1b[38;2;183;0;71m█\x1b[38;2;179;0;75m█\x1b[38;2;175;0;79m╔\x1b[38;2;171;0;83m╝\x1b[38;2;167;0;87m \x1b[38;2;163;0;91m█\x1b[38;2;158;0;96m█\x1b[38;2;154;0;100m║\x1b[38;2;150;0;104m \x1b[38;2;146;0;108m \x1b[38;2;142;0;112m \x1b[38;2;137;0;117m \x1b[38;2;133;0;121m╚\x1b[38;2;129;0;125m█\x1b[38;2;125;0;129m█\x1b[38;2;121;0;133m█\x1b[38;2;117;0;137m█\x1b[38;2;112;0;142m█\x1b[38;2;108;0;146m█\x1b[38;2;104;0;150m╗\x1b[38;2;100;0;154m \x1b[38;2;96;0;158m█\x1b[38;2;91;0;163m█\x1b[38;2;87;0;167m█\x1b[38;2;83;0;171m█\x1b[38;2;79;0;175m█\x1b[38;2;75;0;179m█\x1b[38;2;71;0;183m╔\x1b[38;2;66;0;188m╝\x1b[38;2;62;0;192m \x1b[38;2;58;0;196m╚\x1b[38;2;54;0;200m█\x1b[38;2;50;0;204m█\x1b[38;2;45;0;209m█\x1b[38;2;41;0;213m█\x1b[38;2;37;0;217m╔\x1b[38;2;33;0;221m╝\x1b[38;2;29;0;225m \x1b[38;2;25;0;229m \x1b[38;2;20;0;234m \x1b[38;2;16;0;238m█\x1b[38;2;12;0;242m█\x1b[38;2;8;0;246m█\x1b[38;2;4;0;250m╗\x1b[38;2;0;0;255m \x1b[0m\n\x1b[38;2;255;0;0m╚\x1b[38;2;250;0;4m═\x1b[38;2;246;0;8m╝\x1b[38;2;242;0;12m \x1b[38;2;238;0;16m \x1b[38;2;234;0;20m \x1b[38;2;229;0;25m \x1b[38;2;225;0;29m \x1b[38;2;221;0;33m \x1b[38;2;217;0;37m╚\x1b[38;2;213;0;41m═\x1b[38;2;209;0;45m═\x1b[38;2;204;0;50m╝\x1b[38;2;200;0;54m \x1b[38;2;196;0;58m \x1b[38;2;192;0;62m╚\x1b[38;2;188;0;66m═\x1b[38;2;183;0;71m═\x1b[38;2;179;0;75m═\x1b[38;2;175;0;79m╝\x1b[38;2;171;0;83m \x1b[38;2;167;0;87m \x1b[38;2;163;0;91m╚\x1b[38;2;158;0;96m═\x1b[38;2;154;0;100m╝\x1b[38;2;150;0;104m \x1b[38;2;146;0;108m \x1b[38;2;142;0;112m \x1b[38;2;137;0;117m \x1b[38;2;133;0;121m \x1b[38;2;129;0;125m╚\x1b[38;2;125;0;129m═\x1b[38;2;121;0;133m═\x1b[38;2;117;0;137m═\x1b[38;2;112;0;142m═\x1b[38;2;108;0;146m═\x1b[38;2;104;0;150m╝\x1b[38;2;100;0;154m \x1b[38;2;96;0;158m╚\x1b[38;2;91;0;163m═\x1b[38;2;87;0;167m═\x1b[38;2;83;0;171m═\x1b[38;2;79;0;175m═\x1b[38;2;75;0;179m═\x1b[38;2;71;0;183m╝\x1b[38;2;66;0;188m \x1b[38;2;62;0;192m \x1b[38;2;58;0;196m \x1b[38;2;54;0;200m╚\x1b[38;2;50;0;204m═\x1b[38;2;45;0;209m═\x1b[38;2;41;0;213m═\x1b[38;2;37;0;217m╝\x1b[38;2;33;0;221m \x1b[38;2;29;0;225m \x1b[38;2;25;0;229m \x1b[38;2;20;0;234m \x1b[38;2;16;0;238m╚\x1b[38;2;12;0;242m═\x1b[38;2;8;0;246m═\x1b[38;2;4;0;250m╝\x1b[38;2;0;0;255m \x1b[0m\n"
flora_server = Flask("FloraBot", template_folder="FloraBot", static_folder="FloraBot")
flora_host = "127.0.0.1"
flora_port = 3003
framework_address = "127.0.0.1:3000"
bot_qq = 0
administrator = []
auto_install = False

flora_version = "v1.01"
plugins_dict = {}  # 插件对象字典
plugins_info_dict = {}  # 插件信息字典


def load_config():  # 加载FloraBot配置文件函数
    global auto_install, flora_host, flora_port, framework_address, bot_qq, administrator
    if os.path.isfile("./Config.json"):  # 若文件存在
        with open("./Config.json", "r", encoding="UTF-8") as read_flora_config:
            flora_config = json.loads(read_flora_config.read())
        auto_install = flora_config.get("AutoInstallLibraries")
        flora_host = flora_config.get("FloraHost")
        flora_api.update({"FloraHost": flora_host})
        flora_port = flora_config.get("FloraPort")
        flora_api.update({"FloraPort": flora_port})
        framework_address = flora_config.get("FrameworkAddress")
        flora_api.update({"FrameworkAddress": framework_address})
        bot_qq = flora_config.get("BotQQ")
        flora_api.update({"BotQQ": bot_qq})
        administrator = flora_config.get("Administrator")
        flora_api.update({"Administrator": administrator})
    else:  # 若文件不存在
        print("FloraBot 启动失败, 未找到配置文件 Config.json")
        with open("./Config.json", "w", encoding="UTF-8") as write_flora_config:
            write_flora_config.write(json.dumps({"AutoInstallLibraries": True, "FloraHost": "127.0.0.1", "FloraPort": 3003, "FrameworkAddress": "127.0.0.1:3000", "BotQQ": 0, "Administrator": [0]}, ensure_ascii=False, indent=4))
        print("已生成一个新的配置文件 Config.json , 请修改后再次启动 FloraBot")
        exit()


def send_msg(msg: str, uid: str | int, gid: str | int | None, mid: str | int | None = None):  # 发送信息函数,msg: 正文,uid: QQ号,gid: 群号,mid: 消息编号
    url = f"http://{framework_address}"
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
        requests.post(url, json=data, timeout=5)  # 提交发送消息
    except requests.exceptions.RequestException:
        pass


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


def update_flora_api():  # 更新API内容函数
    # noinspection PyTypeChecker
    flora_api.update({"PluginsDict": plugins_dict.copy(), "PluginsInfoDict": plugins_info_dict.copy()})
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


flora_api = {"FloraPath": os.path.dirname(os.path.abspath(__file__)), "FloraHost": flora_host, "FloraPort": flora_port, "FrameworkAddress": framework_address, "BotQQ": bot_qq, "Administrator": administrator, "FloraVersion": flora_version, "FloraServer": flora_server, "UpdateFloraApi": update_flora_api, "LoadPlugins": load_plugins, "SendMsg": send_msg}


@flora_server.post("/")
def process():  # 消息处理函数,不要主动调用这个函数
    data = request.get_json()  # 获取提交数据
    uid = data.get("user_id")
    if uid in administrator:  # 判断消息是否来自于管理员(主人)
        gid = data.get("group_id")
        mid = data.get("message_id")
        msg = data.get("raw_message")
        if msg is not None:
            msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
            if msg == "/重载插件":
                send_msg("正在重载插件, 请稍后...", uid, gid, mid)
                load_plugins()
                send_msg(f"FloraBot {flora_version}\n\n插件重载完成, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid)
            elif msg == "/插件列表":
                plugins = f"FloraBot {flora_version}\n\n插件列表:\n"
                for plugin_info in plugins_info_dict.values():
                    plugin_status = "启用"
                    if not plugin_info.get("EnablePlugin"):
                        plugin_status = "禁用"
                    plugins += f"•{plugin_info.get('PluginName')}  [状态: {plugin_status}]\n"
                plugins += f"\n共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件\n可使用 \"/启用/禁用插件 + [插件名]\" 来启用或者禁用插件\n若未找到插件, 但插件文件已添加, 请试试使用 \"/重载插件\""
                send_msg(plugins, uid, gid, mid)
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
                    send_msg(f"FloraBot {flora_version}\n\n插件 {msg} 已启用, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid)
                else:
                    send_msg(f"FloraBot {flora_version}\n\n未找到或已启用插件 {msg} , 若未找到插件, 但插件文件已添加, 请试试使用 \"/重载插件\"", uid, gid, mid)
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
                    send_msg(f"FloraBot {flora_version}\n\n插件 {msg} 已禁用, 共有 {len(plugins_info_dict)} 个插件, 已启用 {len(plugins_dict)} 个插件", uid, gid, mid)
                else:
                    send_msg(f"FloraBot {flora_version}\n\n未找到或已禁用插件 {msg} , 若未找到插件, 但插件文件已添加, 请试试使用 \"/重载插件\"", uid, gid, mid)
            elif msg.startswith("/echo "):
                send_msg(msg.replace("/echo ", "", 1), uid, gid, mid)
            elif msg.startswith("/echo1 "):
                send_msg(msg.replace("/echo1 ", "", 1), uid, gid)
    for plugin in plugins_dict.values():  # 遍历开线程调用所有的插件事件函数
        try:
            threading.Thread(target=plugin.event, args=(data,)).start()
        except AttributeError:
            pass
    return "OK"


def check_privileges():
    system = platform.system()
    print(f"当前系统为 {system}")
    if system == "Windows":
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            is_admin = False
        if is_admin:
            print("\033[91m警告: 当前用户具有管理员权限, 若是添加了恶意插件, 后果不堪设想!!!\033[0m")
    elif system in ["Linux", "Darwin"]:
        if os.geteuid() == 0:
            print("\033[91m警告: 当前用户具有 root 权限, 若是添加了恶意插件, 后果不堪设想!!!\033[0m")


if __name__ == "__main__":
    print(flora_logo)
    check_privileges()
    print("正在初始化 FloraBot , 请稍后...")
    if not os.path.isdir("./FloraBot"):
        os.makedirs("./FloraBot")
    if not os.path.isdir("./FloraBot/Plugins"):
        os.makedirs("./FloraBot/Plugins")
    load_config()
    print(f"欢迎使用 FloraBot {flora_version}")
    print("\033[93m声明: 插件为第三方内容, 请您自行分辨是否为恶意插件, 若被恶意插件入侵/破坏了您的设备或恶意盗取了您的信息, 造成的损失请自负, FloraBot 作者概不负责也无义务负责!!!\033[0m")
    load_plugins()
    flora_server.run(host=flora_host, port=flora_port)
