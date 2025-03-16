<p align="center">
  <img src="https://github.com/florabotteam.png" width="200" height="200" alt="FloraBot Logo">
</p>

<div align="center">

# FloraBot

✨ 一个新的, 使用 Python 编写的支持插件的 ChatBot ✨

</div>

<p align="center">
  <a href="https://github.com/FloraBotTeam/FloraBot/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-GPL3.0-green" alt="license">
  </a>
  <a href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3.11-blue?logo=Python" alt="python">
  </a>
  <a href="https://github.com/FloraBotTeam/FloraBot/releases">
    <img src="https://img.shields.io/github/v/release/FloraBotTeam/FloraBot" alt="release">
  </a>
</p>

<p align="center">
  <a href="https://florabotteam.github.io">📖Docs</a>
</p>

## 介绍

FloraBot是一个功能强大的聊天机器人，旨在为用户提供智能、便捷的聊天服务。以下是FloraBot的主要特点：

- **方便快捷**：FloraBot支持多个平台，旨在提供更加简便快捷的服务
- **拓展方便**: Florabot允许用户自行开发和安装插件来拓展功能,并且开发难度低

## 快速开始

1. **安装Python**
   - Windows用户前往[Python官网](https://www.python.org/downloads)下载不低于`Python3.11`的版本进行安装。
   - Linux用户运行命令`apt install python3`，可将`python3`改为指定版本，如`python3.11`。

2. **下载FloraBot**
   - 点击GitHub仓库右上角的绿色`Code`按钮，选择`Download ZIP`下载，或通过链接下载[FloraBot源码](https://github.com/FloraBotTeam/FloraBot/archive/main.zip)。

3. **解压文件**
   - 解压下载的文件后，可删除`PluginTemplate`文件夹（开发者可保留）。

4. **创建启动脚本**
   - **Windows用户**：在`FloraBot.py`同级目录创建文本文档，内容为`python FloraBot.py`，保存后将后缀名改为`.bat`，双击运行。若无法运行Python，需将脚本内容改为Python.exe的绝对路径。
   - **Linux用户**：在`FloraBot.py`同级目录创建`.sh`文件，内容为`python3 FloraBot.py`，可将`python3`改为指定版本，如`python3.11`。

5. **安装必要库**
   - 打开终端（Windows使用CMD或PowerShell），运行以下命令安装所有必要库：
     ```Shell
     pip install -r requirements.txt文件所在路径
     ```
   - 若手动安装，依次运行以下命令：
     ```Shell
     pip install flask
     pip install requests
     pip install websocket-server
     pip install colorama
     ```
   - 若`pip`命令无法运行，可尝试将`pip`替换为`python3 -m pip`。

6. **首次启动与配置**
   - 首次启动会失败，但会在`FloraBot.py`同级目录生成`Config.json`文件，编辑该文件进行配置。

## 配置说明

`Config.json`文件的键值对照表如下：

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

- **`AutoInstallLibraries`**：是否自动安装pip安装所需的第三方库，默认为`true`。
- **`ConnectionType`**：Bot与框架的连接方式，可选`HTTP`和`WebSocket`，默认为`HTTP`。
- **`FloraHost`**：Bot监听的IP地址，默认为`127.0.0.1`。
- **`FloraPort`**：Bot监听的端口号，默认为`3003`。
- **`FrameworkAddress`**：框架的Http协议监听地址，格式为`IP地址:端口号`，默认为`127.0.0.1:3000`。
- **`BotID`**：登录的Bot账号的ID，默认为`0`。
- **`Administrator`**：管理员/所有者/主人的ID列表，格式为`[ID, ID, ...]`，默认为`[0]`。

## 再次启动

完成配置后，再次启动FloraBot，若无意外，已可正常使用。

## 注意事项

部分框架使用WebSocket协议进行连接，Bot可能会警告WebSocket相关的问题。如果能够正常收发消息，请忽略警告；如果不能，则可能是框架的问题。

## 框架配置

- **Http协议配置**：框架需要开启Http服务，启用Http事件上报，关闭Http心跳（避免出现Bug），并在事件上报地址中添加Bot的监听地址。若框架支持消息上报格式，设置为`CQ码`即可。
- **WebSocket协议配置**：Bot仅支持反向WebSocket，因此框架应配置反向WebSocket，其他部分与HTTP协议配置相同。

## 添加插件

**重要声明**：插件为第三方内容，请自行分辨是否为恶意插件。若因恶意插件导致设备受损或信息泄露，FloraBotTeam概不负责。

首次启动会创建一个名为`FloraBot`的文件夹，进入该文件夹，再进入`Plugins`文件夹，将插件文件夹放入其中。若插件为压缩包，需解压后再放入。

文件结构示例：
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

## 内置功能

与Bot账号私聊或在Bot加入的群聊中发送指令触发：

- **`/重载插件`**：重新加载插件，若在FloraBot运行中添加/删除/修改了插件文件，请发送该指令重新加载。
- **`/插件列表`**：发送该指令后，Bot会自动发送当前已添加的所有插件的列表，包括插件的状态等。
- **`/启用插件 + [空格] + [插件名]`**：若插件被禁用，可使用该指令启用插件，插件名可通过`/插件列表`指令查询。
- **`/禁用插件 + [空格] + [插件名]`**：若不想要该插件的功能，可使用该指令禁用插件，插件名可通过`/插件列表`指令查询。
- **`/echo + [空格] + [内容]`**：让Bot复读一遍内容，用于调试（Debug），此指令复读方式为回复。
- **`/echo1 + [空格] + [内容]`**：与`/echo`功能相同，只是复读方式不为回复。
- **`/帮助`**：查看FloraBot可使用的指令。
- **`/帮助 + [空格] + [插件名]`**：可查看对应插件的帮助。

## 插件开发

**要求**：
- 会Python的基础知识。
- 会使用Python解析Json。
- 如果会CQ码会更好。

**示例模板**：可在仓库中的`PluginTemplate`文件夹内找到模板。

**`Plugin.json`（必要）**：
```Json
{
    "PluginName": "插件名",
    "PluginVersion": "插件版本",
    "DependentLibraries": null,
    "IsLibraries": false,
    "PluginIcon": null,
    "PluginAuthor": "插件作者名",
    "MainPyName": "插件主.py文件名，不要带上.py后缀名",
    "PluginDescription": "插件描述",
    "EnablePlugin": true,

    "Help": [
        {
            "Class": "分类",
            "Commands": [
                {
                    "Command": "指令",
                    "Content": "指令介绍"
                }
            ]
        }
    ]
}
```

**`Plugin.json`文件键值对照表**：
- **`PluginName`**：插件名。
- **`PluginVersion`**：插件版本。
- **`DependentLibraries`**：依赖的第三方库的名称，若`AutoInstallLibraries`值为`true`，则会尝试自动安装这些库，格式为`["库名", "库名", ...]`。
- **`IsLibraries`**：是否为依赖库插件。
- **`PluginIcon`**：插件的图标，格式为`xxx.png`（要带上后缀，主流文件格式即可，可以在文件夹下，但相对路径是从`Plugin.json`文件所在的目录开始的）。
- **`PluginAuthor`**：插件作者名。
- **`MainPyName`**：插件主.py文件名，不要带上.py后缀名，另外py文件里不要赋值`__name__`变量！
- **`PluginDescription`**：插件描述。
- **`EnablePlugin`**：是否启用插件，这是一个标志，用于启用和禁用插件，默认值为`true`即可。
- **`Help`**：帮助菜单内容列表。
- **`Class`**：指令分类。
- **`Commands`**：分类的指令列表。
- **`Command`**：指令。
- **`Content`**：指令介绍。

**Python文件（必要）示例**：

```Python
# 前言，这里用不到的函数可以不定义，可以直接删去，包括API也可以删去不定义，不会报错的

flora_api = {}  # 顾名思义，FloraBot的API，载入（若插件已设为禁用则不载入）后会赋值上


def occupying_function(*values):  # 该函数仅用于占位，并没有任何意义
    pass


send_msg = occupying_function


def init():  # 插件初始化函数，在载入（若插件已设为禁用则不载入）或启用插件时会调用一次，API可能没有那么快更新，可等待，无传入参数
    global send_msg
    print(flora_api)
    send_msg = flora_api.get("SendMsg")
    print("FloraBot插件模板 加载成功")


def api_update_event():  # 在API更新时会调用一次（若插件已设为禁用则不调用），可及时获得最新的API内容，无传入参数
    print(flora_api)


def event(data: dict):  # 事件函数，FloraBot每收到一个事件都会调用这个函数（若插件已设为禁用则不调用），传入原消息JSON参数
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

**注意事项**：
- 这些函数以及`flora_api`变量都不是必要的，少了也不会报错。
- `init`函数里获取API内容的话，`PluginsDict`和`PluginsInfoDict`还不是正确的，推荐放到`api_update_event`函数中处理。

## 插件API

这些在插件中都可以使用`flora_api.get()`获取到：

- **`FloraPath`**：FloraBot.py文件所在的绝对路径，不是这个文件的路径，而是所在目录。
- **`FloraHost`**：Bot监听的IP地址。
- **`FloraPort`**：Bot监听的端口号。
- **`FrameworkAddress`**：QQ框架的Http协议监听地址。
- **`BotID`**：登录的Bot账号的ID。
- **`Administrator`**：管理员/所有者/主人的ID列表。
- **`FloraVersion`**：Bot的版本号。
- **`FloraServer`**：Bot的Flask实例。
- **`UpdateFloraApi`**：更新`flora_api`的函数，调用了会同时调用插件中的`api_update_event`函数，无参数。
- **`LoadPlugins`**：加载/重载插件函数，会调用`UpdateFloraApi`函数，无参数。
- **`BroadcastEvent`**：广播消息函数，向所有插件包括内置功能广播基于OneBot协议的数据，参数如下方注释解释：
  ```Python
  def broadcast_event(data: dict, send_type: str, ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):
      # 广播消息函数，data: 基于OneBot协议的数据
      # send_type: 发送类型，告诉插件是用HTTP还是WebSocket发送消息
      # ws_client: WebSocket连接实例，ws_server: WebSocket服务端实例（若发送类型为WebSocket这两个参数必填）
      # send_host: HTTP协议发送地址，send_port: HTTP协议发送端口（若填这两个参数则使用自定义地址发送）
  ```
  **调用示例**：
  - HTTP：
    ```Python
    broadcast_event(data, "HTTP")
    ```
  - WebSocket：
    ```Python
    broadcast_event(data, "WebSocket", ws_client, ws_server)
    ```
- **`SendMsg`**：发送信息函数，也可以发送事件，只要你会CQ码，参数如下方注释解释：
  ```Python
  def send_msg(msg: str, uid: str | int, gid: str | int | None, mid: str | int | None = None, ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):
      # 发送消息函数，send_type: 发送类型，决定是用HTTP还是WebSocket发送消息
      # msg: 正文，uid: ID，gid: 群号，mid: 消息编号
      # ws_client: WebSocket连接实例，ws_server: WebSocket服务端实例（若发送类型为WebSocket这两个参数必填）
      # send_host: HTTP协议发送地址，send_port: HTTP协议发送端口（若填这两个参数则使用自定义地址发送）
  ```
  **关于`SendMsg`的补充**：默认传入参数如下即可：
  ```Python
  send_msg(send_type, "正文", uid, gid, mid, ws_client, ws_server, send_host, send_port)
  ```
  默认为回复信息，如果不需要回复将参数`mid`改成`None`即可。调用函数后会返回相应的信息（dict类型），有需求可获取其中的数据（如获取该消息的mid，可用于撤回该消息）。
- **`CallApi`**：向框架调用API，会返回dict类型的数据，参数与`SendMsg`差不多，函数如下：
  ```Python
  def call_api(send_type: str, api: str, params: dict, ws_client=None, ws_server=None, send_host: str = "", send_port: int | str = ""):
      # 发送消息函数，send_type: 发送类型，决定是用HTTP还是WebSocket发送消息
      # api: 接口/终结点去掉"/"（str类型），data: 数据（dict类型）
      # ws_client: WebSocket连接实例，ws_server: WebSocket服务端实例（若发送类型为WebSocket这两个参数必填）
      # send_host: HTTP协议发送地址，send_port: HTTP协议发送端口（若填这两个参数则使用自定义地址发送）
  ```
  **API（终结点）以及该API的参数查阅OneBot文档调用**，调用函数后会返回相应的信息（dict类型），有需求可获取其中的数据。以下是调用示例：
  ```Python
  print(call_api(send_type, "API", {}, ws_client, ws_server, send_host, send_port))
  ```
- **`HelpInfoDict`**：所有插件包括FloraBot的帮助字典。
- **`CallApiReturned`**：调用框架API时，如果为WebSocket协议，这里将会记录返回的数据。这个逻辑也相对地引出了新的Bug，当插件以WebSocket协议广播消息时，若其他插件会发送消息或调用API时会等待WebSocket返回调用参数返回的数据，因为是插件广播的，所以会一直永远的等待下去。若插件有这个需求，还请查看源代码进行开发。作者已经尽力了（一般绝对用不上，要用请参考源代码）。
- **`PluginsDict`**：插件对象字典，使用对应的插件名获取，并赋值给变量（或不赋值直接调用），即可将对应的插件当作库来调用。
- **`PluginsInfoDict`**：插件信息字典，使用对应的插件名获取，可获取到对应插件的`Plugin.json`已转换为Python对象的内容。
- **`ThePluginPath`**：插件对于`FloraBot.py`文件所在的目录的相对路径。由于是将插件导入再调用的，所以任何相对路径都是从`FloraBot.py`文件所在的目录开始的。这非常重要，不推荐使用自己手动定义到插件资源的相对路径，而是推荐使用`ThePluginPath` + 插件相对于资源的相对路径（因为可能会出现种种原因导致你手动定义到插件资源的相对路径不能正确使用插件文件夹中的文件）。示例：我有一个叫做Test.json的文件，在插件目录中的文件夹Test中（即Test/Test.json），那么获取`ThePluginPath`的值拼接到路径"/Test/Test.json"的前面即可获得`FloraBot.py`与该文件的相对路径，现在就可以在插件中正确地使用这个文件了（希望不会那么拗口：)）。
  **如果还是不能理解`ThePluginPath`的话，直接上代码**：
  ```Python
  import json

  group_white_list = []


  def init():
      global group_white_list
      with open(f"./{flora_api.get('ThePluginPath')}/Plugin.json", "r", encoding="UTF-8") as plugin_config:
          group_white_list = json.loads(plugin_config.read()).get("GroupWhiteList")
  ```
  上述代码使用`ThePluginPath`拼接了当前插件配置文件的路径，并且读取并获取了当中的`GroupWhiteList`键的值。
  另外，如果要发送图片等本地文件需要绝对路径可以这么写：
  ```Python
  flora_api = {}


  def occupying_function(*values):  # 该函数仅用于占位，并没有任何意义
      pass


  send_msg = occupying_function


  def init():
      global send_msg
      send_msg = flora_api.get("SendMsg")


  def event(data: dict):  # 事件函数，FloraBot每收到一个事件都会调用这个函数（若插件已设为禁用则不调用），传入原消息JSON参数
      print(data)
      send_type = data.get("SendType")
      send_address = data.get("SendAddress")
      ws_client = send_address.get("WebSocketClient")
      ws_server = send_address.get("WebSocketServer")
      send_host = send_address.get("SendHost")
      send_port = data.get("SendPort")
      uid = data.get("user_id")  # 事件对象QQ号
      gid = data.get("group_id")  # 事件对象群号
      mid = data.get("message_id")  # 消息ID
      msg = data.get("raw_message")  # 消息内容
      if msg is not None:
          msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
          if msg == "TestSendImage":
              send_msg(send_type, f"[CQ:image,file=file:///{flora_api.get('FloraPath')}/{flora_api.get('ThePluginPath')}/Test.png]", uid, gid, mid, ws_client, ws_server, send_host, send_port)
  ```
  上述代码发送图片时使用了`FloraPath`和`ThePluginPath`拼接了当前插件文件夹下的Test.png的绝对路径，或获取相对路径的文件的绝对路径。
  **注意!!!**：拼接路径请使用`/`而不是`\`，因为如果路径中出现了`\`则只能在Windows中使用，而`/`则是全平台，Windows支持使用`/`拼接路径。

## 推荐QQ框架

- **[NapNeko/NapCatQQ](https://github.com/NapNeko/NapCatQQ)**

## 关于

**QQ群（仅供开发者加入）：[994825372](http://qm.qq.com/cgi-bin/qm/qr?group_code=994825372)**
