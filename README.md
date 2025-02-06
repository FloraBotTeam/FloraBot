# FloraBot
**一个新的, 使用 Python 编写的支持插件的 ChatBot**
## 官方文档(更新可能不及时, 建议耐心查看仓库文档)
* **[`https://florabotteam.github.io`](https://florabotteam.github.io)**
## 一键安装脚本
**[`https://github.com/FloraBotTeam/FloraBot-Installer`](https://github.com/FloraBotTeam/FloraBot-Installer)**
## 食用方法(面向小白)
1. **Windows: 前往 [`Python官网`](https://www.python.org/downloads) 下载不低于 `Python3.11` 的版本进行安装, Linux: 运行命令**
```Shell
apt install python3
```
**可将 python3 改为一个指定的版本, 如作者喜欢用的 python3.11**  
2. **点击右上角 About 左边的绿色的 `Code` 按钮, 再点击 `Download ZIP` 下载亦或者通过链接下载(请 clone 仓库, 不要使用 release 的版本, 因为它过于老旧)[`https://github.com/FloraBotTeam/FloraBot/archive/main.zip`](https://github.com/FloraBotTeam/FloraBot/archive/main.zip)**  
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
**Bot 内置了一些功能(除 `/插件列表` 和 `/帮助` 外都需要账号的 ID 在 `Administrator` 列表内才能够触发):**  
* **`/重载插件`: 重新加载插件, 若在 FloraBot 运行中添加/删除/修改了插件文件, 请发送该指令重新加载一下插件**  
* **`/插件列表`: 发送该指令后 Bot 会自动发送当前已添加的所有插件的列表, 包括插件的状态等**  
* **`/启用插件 + [空格] + [插件名]`: 若插件被禁用了可启用插件, 插件名可使用 `/插件列表` 指令查询**  
* **`/禁用插件 + [空格] + [插件名]`: 若不想要该插件的功能了可禁用插件, 插件名可使用 `/插件列表` 指令查询**
* **`/echo + [空格] + [内容]`: 让 Bot 复读一遍内容, 用于调试(Debug), 这个指令复读方式为回复**
* **`/echo1 + [空格] + [内容]`: 与 `/echo` 功能是相同的, 只是复读方式不为回复**  
* **`/帮助`: 查看 FloraBot 可使用的指令**  
* **`/帮助 + [空格] + [插件名]`: 可查看对应插件的帮助**
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
    "PluginVersion": "插件版本",
    "DependentLibraries": null,
    "IsLibraries": false,
    "PluginIcon": null,
    "PluginAuthor": "插件作者名",
    "MainPyName": "插件主 .py 文件名, 不要带上 .py 后缀名",
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
**`Plugin.json` 文件键值对照表:**  
* **`PluginName`: 插件名**  
* **`PluginVersion`: 插件版本**  
* **`DependentLibraries`: 依赖的第三方库的名称, 若 `AutoInstallLibraries` 值为 `true` 则会尝试自动安装这些库, 格式为: `["库名", "库名", ...]`**  
* **`IsLibraries`: 是否为依赖库插件**  
* **`PluginIcon`: 插件的图标, 格式为: `xxx.png`(要带上后缀