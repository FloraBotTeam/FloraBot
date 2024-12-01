# FloraBot
**一个新的, 使用 Python 编写的支持插件的 ChatBot**
## 官方文档
* **[`https://florabotteam.github.io`](https://florabotteam.github.io)**
## 一键安装脚本
**[`https://github.com/FloraBotTeam/FloraBot-Installer`](https://github.com/FloraBotTeam/FloraBot-Installer)**
## 食用方法(面向小白)
1. **Windows: 前往 [`Python官网`](https://www.python.org/downloads) 下载不低于 `Python3.11` 的版本进行安装, Linux: 运行命令**
```Shell
apt install python3
```
**可将 python3 改为一个指定的版本, 如作者喜欢用的 python3.11**  
2. **点击右上角 About 左边的绿色的 `Code` 按钮, 再点击 `Download ZIP` 下载亦或者通过链接下载[`https://github.com/FloraBotTeam/FloraBot/archive/main.zip`](https://github.com/FloraBotTeam/FloraBot/archive/main.zip)**  
3. **用户解压后可删去 `PluginTemplate` 文件夹, 开发者可保留**  
4. **如果是 Windows 用户, 在文件 `FloraBot.py` 的同级目录可创建一个文本文档, 内容为**  
```Shell
python FloraBot.py
```
**然后保存, 再重命名文件, 将后缀名 `.txt` 改为 `.bat`双击运行一下**  
**若无法运行, 找到你安装 Python 的路径, 再找到 `python.exe` 将脚本内容改为**  
```Shell
python.exe的绝对路径 FloraBot.py
```
**保存然后再运行**  
**如果是 Linux 用户, 在文件 `FloraBot.py` 的同级目录可创建一个后缀名为 `.sh` 的文件, 内容为**  
```Shell
python3 FloraBot.py
```
**使用 python3 命令不一定可以运行, 可改为一个指定的版本, 如 python3.11**  
**安装必要的库:**  
**若想一行指令安装所有必要库, 运行以下命令:**  
```Shell
pip install -r requirements.txt文件所在路径
```
**若使用手动安装, 则运行以下命令:**  
* **`flask`**
```Shell
pip install flask
```
* **`requests`**
```Shell
pip install requests
```
* **`websocket-server`**
```Shell
pip install websocket-server
```
**使用 pip 命令不一定可以运行, 可尝试将 pip 换成 python3 -m pip**  
**运行脚本**  
5. **首次启动会启动失败, 此时会在文件 `FloraBot.py` 的同级目录下生成一个 `Config.json` 文件, 编辑它**
## 配置
**`Config.json`:**  
```Json
{
    "AutoInstallLibraries": true,
    "ConnectionType": "HTTP",
    "FloraHost": "127.0.0.1",
    "FloraPort": 3003,
    "FrameworkAddress": "127.0.0.1:3000",
    "BotID": 0,
    "Administrator": [0]
}
```
**`Config.json` 文件键值对照表:**  
* **`AutoInstallLibraries`: 是否自动安装 pip 安装所需的第三方库, 默认为值: `true`**  
* **`ConnectionType`: Bot 与框架的连接方式, 可选 `HTTP` 和 `WebSocket`, 默认值为: `HTTP`**  
**(Bot 只支持反向 WebSocket 呢)**  
* **`FloraHost`: Bot 监听的 IP 地址, 默认值为: `127.0.0.1`**  
* **`FloraPort`: Bot 监听的端口号, 默认值为: `3003`**  
**(Http 协议配置, 请在框架中将 Http 上报打开并且添加上报地址为: `http://FloraHost:FloraPort`)**  
**(反向 WebSocket 协议配置, 请在框架中将 反向WebSocket 服务打开并且添加地址为: `ws://FloraHost:FloraPort`)**  
* **`FrameworkAddress`: 框架的 Http 协议监听地址, 格式为: `IP地址:端口号`, 默认值为: `127.0.0.1:3000`**  
* **`BotID`: 登录的 Bot 账号的 ID, 默认值为 `0`**  
* **`Administrator`: 管理员/所有者/主人的 ID 列表, 一些特殊的功能需要该账号的 ID 在此列表内才能够触发, 格式为: `[ID, ID, ...]`, 默认值为: `[0]`**  
6. **再次启动, 不出意外的话, 已经可以正常使用了**  
## 注意
**部分框架使用 WebSocket 协议进行连接, Bot 可能会警告 WebSocket 相关的问题, 如果能够正常收发消息请忽略, 如果不能则为框架的问题**    
## 框架配置
**Http 协议配置, 框架需要把 Http 服务打开, 启用 Http 事件上报, 关闭 Http 心跳(一定要关, 不然会出现意想不到的 Bug), 然后在事件上报地址中添加 Bot 的监听地址, 如果有消息上报格式, 设置为 `CQ码` 即可**  
**WebSocket 协议配置, Bot 只支持反向 WebSocket , 所以框架应该配置反向 WebSocket 哦, 其他部分与 HTTP 协议配置相同**  
## 添加插件
***声明: 插件为第三方内容, 请您自行分辨是否为恶意插件, 若被恶意插件入侵/破坏了您的设备或恶意盗取了您的信息, 造成的损失请自负, FloraBotTeam 概不负责也无义务负责!!!***  
***声明: 插件为第三方内容, 请您自行分辨是否为恶意插件, 若被恶意插件入侵/破坏了您的设备或恶意盗取了您的信息, 造成的损失请自负, FloraBotTeam 概不负责也无义务负责!!!***  
***声明: 插件为第三方内容, 请您自行分辨是否为恶意插件, 若被恶意插件入侵/破坏了您的设备或恶意盗取了您的信息, 造成的损失请自负, FloraBotTeam 概不负责也无义务负责!!!***  
**重要的事情说三遍!!!**  
  
**首次启动会创建一个名为 `FloraBot` 的文件夹, 进入这个文件夹, 再进入 `Plugins` 文件夹, 将插件文件夹放入 `Plugins` 文件夹, 若是压缩了, 解压再放入即可**  
**文件结构示意:**  
```File
FloraBot
 \-Plugins
    |-插件文件夹
    |  |-Plugin.json
    |  \-插件.py
    \-插件文件夹
       |-Plugin.json
       \-插件.py
Config.json
FloraBot.py
启动脚本
```
## 内置功能(与 Bot 账号私聊或在 Bot 加入的群聊中发送指令触发)
**Bot 内置了一些功能(都需要账号的 ID 在 `Administrator` 列表内才能够触发):**  
* **`/重载插件`: 重新加载插件, 若在 FloraBot 运行中添加/删除/修改了插件文件, 请发送该指令重新加载一下插件**  
* **`/插件列表`: 发送该指令后 Bot 会自动发送当前已添加的所有插件的列表, 包括插件的状态等**  
* **`/启用插件 + [空格] + 插件名`: 若插件被禁用了可启用插件, 插件名可使用 `/插件列表` 指令查询**  
* **`/禁用插件 + [空格] + 插件名`: 若不想要该插件的功能了可禁用插件, 插件名可使用 `/插件列表` 指令查询**
* **`/echo + [空格] + [内容]`: 让 Bot 复读一遍内容, 用于调试(Debug), 这个指令复读方式为回复**
* **`/echo1 + [空格] + [内容]`: 与 `/echo` 功能是相同的, 只是复读方式不为回复**
## 插件开发
**要求:**  
* **会 Python 的基础知识**  
* **会使用 Python 解析 Json**  
* **如果会 CQ 码会更好**  
* **...**  
**示范(可从仓库中的 `PluginTemplate` 文件夹内找到模板):**  
**`Plugin.json`(必要):**  
```Json
{
    "PluginName": "插件名",
    "DependentLibraries": null,
    "IsLibraries": false,
    "PluginIcon": null,
    "PluginAuthor": "插件作者名",
    "MainPyName": "插件主 .py 文件名, 不要带上 .py 后缀名",
    "PluginDescription": "插件描述",
    "EnablePlugin": true
}
```
**`Plugin.json` 文件键值对照表:**  
* **`PluginName`: 插件名**  
* **`DependentLibraries`: 依赖的第三方库的名称, 若 `AutoInstallLibraries` 值为 `true` 则会尝试自动安装这些库, 格式为: `["库名", "库名", ...]`**  
* **`IsLibraries`: 是否为依赖库插件**  
* **`PluginIcon`: 插件的图标, 格式为: `xxx.png`(要带上后缀, 主流文件格式即可, 可以在文件夹下, 但是相对路径是从 `Plugin.json` 文件所在的目录开始的)**  
* **`PluginAuthor`: 插件作者名**  
* **`MainPyName`: 插件主 .py 文件名, 不要带上 .py 后缀名, 另外 py 文件里不要赋值 `__name__` 变量!**  
* **`PluginDescription`: 插件描述**  
* **`EnablePlugin`: 是否启用插件, 这是一个标志, 用于启用和禁用插件的, 默认值为 `true` 即可**  
## 前言
**目前 WebSocket 协调连接可能调用一些 API 尚存一些问题, 一些框架的 API 调用起来可能会比较复杂, 为了适配 WebSocket 我已经修了很多 Bug 了, 目前做不到把它变得更加完美**  
**但是我已经尽力将接收和发送消息那一块把 HTTP 和 WebSocket 协议给统一了, 一个函数即可解决两种协议的消息发送**  
**py文件(必要)示范:**  
**前言, 这里用不到的函数可以不定义, 可以直接删去, 包括API也可以删去不定义, 不会报错的**
```Python
# 前言,这里用不到的函数可以不定义,可以直接删去,包括API也可以删去不定义,不会报错的

flora_api = {}  # 顾名思义,FloraBot的API,载入(若插件已设为禁用则不载入)后会赋值上


def occupying_function(*values):  # 该函数仅用于占位,并没有任何意义
    pass


send_msg = occupying_function


def init():  # 插件初始化函数,在载入(若插件已设为禁用则不载入)或启用插件时会调用一次,API可能没有那么快更新,可等待,无传入参数
    global send_msg
    print(flora_api)
    send_msg = flora_api.get("SendMsg")
    print("FloraBot插件模板 加载成功")


def api_update_event():  # 在API更新时会调用一次(若插件已设为禁用则不调用),可及时获得最新的API内容,无传入参数
    print(flora_api)


def event(data: dict):  # 事件函数,FloraBot每收到一个事件都会调用这个函数(若插件已设为禁用则不调用),传入原消息JSON参数
    print(data)
    send_type = data.get("SendType")
    send_address = data.get("SendAddress")
    ws_client = send_address.get("WebSocketClient")
    ws_server = send_address.get("WebSocketServer")
    send_host = send_address.get("SendHost")
    send_port = send_address.get("SendPort")
    uid = data.get("user_id")  # 事件对象QQ号
    gid = data.get("group_id")  # 事件对象群号
    mid = data.get("message_id")  # 消息ID
    msg = data.get("raw_message")  # 消息内容
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        print(send_type, uid, gid, mid, msg, ws_client, ws_server, send_host, send_port)
```
**上面的注释已经很详细了**  
**注意事项:**  
* **这些函数以及 `flora_api` 变量都不是必要的, 少了也不会报错**  
* **`init` 函数里获取 API 内容的话, `PluginsDict` 和 `PluginsInfoDict` 还不是正确的, 推荐放到 `api_update_event` 函数中处理**  
## 插件API
**这些在插件中都可以使用 `flora_api.get()` 获取到**  
* **`FloraPath`: FloraBot.py 文件所在的绝对路径, 不是这个文件的路径, 而是所在目录**  
* **`FloraHost`: Bot 监听的 IP 地址**  
* **`FloraPort`: Bot 监听的端口号**  
* **`FrameworkAddress`: QQ 框架的 Http 协议监听地址**  
* **`BotID`: 登录的 Bot 账号的 ID**  
* **`Administrator`: 管理员/所有者/主人的 ID 列表**  
* **`FloraVersion`: Bot 的版本号**  
* **`FloraServer`: Bot 的 Flask 实例**  
* **`UpdateFloraApi`: 更新 `flora_api` 的函数, 调用了会同时调用插件中的 `api_update_event` 函数, 无参数**  
* **`LoadPlugins`: 加载/重载插件函数, 会调用 `UpdateFloraApi` 函数, 无参数**
* **`BroadcastEvent`: 广播消息函数, 向所有插件包括内置功能广播基于 OneBot 协议的数据, 参数如下方注释解释**
```Python
def broadcast_event(data: dict, send_type: str, ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):
    # 广播消息函数,data: 基于OneBot协议的数据
    # send_type: 发送类型,告诉插件是用HTTP还是WebSocket发送消息
    # ws_client: WebSocket连接实例,ws_server: WebSocket服务端实例(若发送类型为WebSocket这两个参数必填)
    # send_host: HTTP协议发送地址,send_port: HTTP协议发送端口(若填这两个参数则使用自定义地址发送)
```
**调用 `BroadcastEvent` 示例:**  
**如果你希望其他插件能够将消息从你的插件中开启的 HTTP 发送消息, 你可以这么写:**  
```Python
broadcast_event(data, "HTTP")
```
**WebSocket:**  
```Python
broadcast_event(data, "WebSocket", ws_client, ws_server)
```
* **`SendMsg`: 发送信息函数, 也可以发送事件, 只要你会 CQ 码, 参数如下方注释解释**  
**`SendMsg` 函数:**  
```Python
def send_msg(msg: str, uid: str | int, gid: str | int | None, mid: str | int | None = None, ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):
    # 发送消息函数,send_type: 发送类型,决定是用HTTP还是WebSocket发送消息
    # msg: 正文,uid: ID,gid: 群号,mid: 消息编号
    # ws_client: WebSocket连接实例,ws_server: WebSocket服务端实例(若发送类型为WebSocket这两个参数必填)
    # send_host: HTTP协议发送地址,send_port: HTTP协议发送端口(若填这两个参数则使用自定义地址发送)
```
**关于 `SendMsg` 的补充, 默认传入参数如下即可:**  
```Python
send_msg(send_type, "正文", uid, gid, mid, ws_client, ws_server, send_host, send_port)
```
**默认为回复信息, 如果不需要回复将参数 `mid` 改成 `None` 即可, 调用了函数后会返回相应的信息(dict类型), 有需求可获取其中的数据(如获取该消息的 mid, 可用于撤回该消息)**  
* **`CallApi`: 向框架调用 API, 会返回 dict 类型的数据, 参数与 `SendMse` 差不多, 函数如下:**  
```Python
def call_api(send_type: str, api: str, params: dict, ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):
    # 发送消息函数,send_type: 发送类型,决定是用HTTP还是WebSocket发送消息
    # api: 接口/终结点去掉"/"(str类型), data: 数据(dict类型)
    # ws_client: WebSocket连接实例,ws_server: WebSocket服务端实例(若发送类型为WebSocket这两个参数必填)
    # send_host: HTTP协议发送地址,send_port: HTTP协议发送端口(若填这两个参数则使用自定义地址发送)
```
**API(终结点) 以及该 API 的参数查阅 OneBot 文档调用, 调用了函数后会返回相应的信息(dict类型), 有需求可获取其中的数据, 以下是调用示范:**  
```Python
print(call_api(send_type, "API", {}, ws_client, ws_server, send_host, send_port))
```
* **`HelpInfoDict`: 所有插件包括 FloraBot 的帮助字典**  
* **`CallApiReturned`: 调用框架 API 时, 如果为 WebSocket 协议, 这里将会记录返回的数据, 这个逻辑也相对的引出了新的 Bug, 当插件以 WebSocket 协议广播消息时, 若其他插件会发送消息或调用 API 时会等待 WebSocket 返回调用参数返回的数据, 因为是插件广播的, 所以会一直永远的等待下去, 若插件有这个需求, 还请查看源代码进行开发, 作者已经尽力了(一般绝对用不上, 要用请参考源代码)**  
* **`PluginsDict`: 插件对象字典, 使用对应的插件名获取, 并赋值给变量(或不赋值直接调用), 即可将对应的插件当作库来调用**  
* **`PluginsInfoDict`: 插件信息字典, 使用对应的插件名获取, 可获取到对应插件的 `Plugin.json` 已转换为 Python 对象的内容**  
* **`ThePluginPath`: 插件对于 `FloraBot.py` 文件所在的目录的相对路径, 由于是将插件导入再调用的, 所以任何相对路径都是从 `FloraBot.py` 文件所在的目录开始的, 这非常重要, 不推荐使用自己手动定义到插件资源的相对路径, 而是推荐使用 `ThePluginPath` + 插件相对于资源的相对路径(因为可能会出现种种原因导致你手动定义到插件资源的相对路径不能正确使用插件文件夹中的文件), 示例: 我有一个叫做 Test.json 的文件, 在插件目录中的文件夹 Test 中(即 Test/Test.json), 那么获取 `ThePluginPath` 的值拼接到路径"/Test/Test.json"的前面即可获得 `FloraBot.py` 与该文件的相对路径, 现在就可以在插件中正确的使用这个文件了(希望不会那么拗口:) )**  
**如果还是不能理解 `ThePluginPath` 的话, 直接上代码:**  
```Python
import json

group_white_list = []


def init():
    global group_white_list
    with open(f"./{flora_api.get('ThePluginPath')}/Plugin.json", "r", encoding="UTF-8") as plugin_config:
        group_white_list = json.loads(plugin_config.read()).get("GroupWhiteList")
```
**上述代码使用 `ThePluginPath` 拼接了当前插件配置文件的路径, 并且读取并获取了当中的 `GroupWhiteList` 键的值**  
**另外, 如果你要发送图片等本地文件需要绝对路径可以这么写:**  
```Python
flora_api = {}


def occupying_function(*values):  # 该函数仅用于占位,并没有任何意义
    pass


send_msg = occupying_function


def init():
    global send_msg
    send_msg = flora_api.get("SendMsg")


def event(data: dict):  # 事件函数,FloraBot每收到一个事件都会调用这个函数(若插件已设为禁用则不调用),传入原消息JSON参数
    print(data)
    send_type = data.get("SendType")
    send_address = data.get("SendAddress")
    ws_client = send_address.get("WebSocketClient")
    ws_server = send_address.get("WebSocketServer")
    send_host = send_address.get("SendHost")
    send_port = send_address.get("SendPort")
    uid = data.get("user_id")  # 事件对象QQ号
    gid = data.get("group_id")  # 事件对象群号
    mid = data.get("message_id")  # 消息ID
    msg = data.get("raw_message")  # 消息内容
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        if msg == "TestSendImage":
            send_msg(send_type, f"[CQ:image,file=file:///{flora_api.get('FloraPath')}/{flora_api.get('ThePluginPath')}/Test.png]", uid, gid, mid, ws_client, ws_server, send_host, send_port)
```
**上述代码发送图片时使用了 `FloraPath` 和 `ThePluginPath` 拼接了当前插件文件夹下的 Test.png 的绝对路径, 或获取相对路径的文件的绝对路径**  
**注意!!!: 拼接路径请使用 `/` 而不是 `\` , 因为如果路径中出现了 `\` 则只能在 Windows 中使用, 而 `/` 则是全平台, Windows 支持使用 `/` 拼接路径**   
### 推荐 QQ 框架
* **[NapNeko/NapCatQQ](https://github.com/NapNeko/NapCatQQ)**
### 作者
* **[`AEBC08`](https://github.com/AEBC08)**
* **BiliBili: [`AEBC08`](https://space.bilibili.com/510197857)**
### 开发交流群
* **QQ群: [`994825372`](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&amp;k=ZkfLbEF4XRGK4Ts044mUdhpFZyn1PtE7&amp;authKey=jAdddExKGHv0ANYh%2BFU634S5SS7jbO6Gr8EJxXRKAVoE7Ue4HpHZdD8tnrOcUSeD&amp;noverify=0&amp;group_code=994825372)**
### Tips
* **作者没什么时间, 如有疑问或建议可提交 Issues**
