import requests
import QQMCBind


# 定义QQ消息的发送函数
def qq_message_send(qqapi_url, group_id, message):
    # 确定要发送给机器人框架处理的数据包，并携带群号、消息等信息
    data = {
        'group_id': group_id,
        'message': message,
        'auto_escape': False
    }
    # 以POST形式访问我们的机器人框架并上传这些数据，让我们的机器人向群里发送消息，从而实现与QQ群的通信
    request = requests.post(qqapi_url, data=data)
    # 将此时的状态返回为request，便于检查与调试
    return request.status_code


# 定义MC服务端内部命令的发送函数，需要借助MCSManager的API
def mc_command_send(qqapi_url, group_id, mcapi_url, uuid, remote_uuid, apikey, command):
    # 这是将要用requests访问的网址，用字符串拼接的方式形成
    if command == 'stop':
        mcapi = "/api/protected_instance/stop"
        http_command = mcapi_url + \
                       mcapi + \
                       '?' + \
                       '&' + 'uuid=' + uuid + \
                       '&' + 'remote_uuid=' + remote_uuid + \
                       '&' + 'apikey=' + apikey
        request = requests.get(http_command)
        if request.status_code == 200:
            qq_message_send(qqapi_url, group_id, "发送成功！")
        elif request.status_code == 400:
            qq_message_send(qqapi_url, group_id, "发送失败，请求参数不正确，请检查配置文件。")
        elif request.status_code == 403:
            qq_message_send(qqapi_url, group_id, "发送失败，权限不够，请检查配置文件。")
        elif request.status_code == 404:
            qq_message_send(qqapi_url, group_id, "未找到后台API，请检查配置文件。")
        elif request.status_code == 500:
            qq_message_send(qqapi_url, group_id, "发送失败，可能是命令正在执行或是后台出现错误。")
        else:
            qq_message_send(qqapi_url, group_id, "发送失败，出现未知错误。")

    elif command == 'start':
        mcapi = "/api/protected_instance/open"
        http_command = mcapi_url + \
                       mcapi + \
                       '?' + \
                       '&' + 'uuid=' + uuid + \
                       '&' + 'remote_uuid=' + remote_uuid + \
                       '&' + 'apikey=' + apikey
        request = requests.get(http_command)
        if request.status_code == 200:
            qq_message_send(qqapi_url, group_id, "发送成功！")
        elif request.status_code == 400:
            qq_message_send(qqapi_url, group_id, "发送失败，请求参数不正确，请检查配置文件。")
        elif request.status_code == 403:
            qq_message_send(qqapi_url, group_id, "发送失败，权限不够，请检查配置文件。")
        elif request.status_code == 404:
            qq_message_send(qqapi_url, group_id, "未找到后台API，请检查配置文件。")
        elif request.status_code == 500:
            qq_message_send(qqapi_url, group_id, "发送失败，可能是命令正在执行或是后台出现错误。")
        else:
            qq_message_send(qqapi_url, group_id, "发送失败，出现未知错误。")
    elif command == 'kill':
        mcapi = "/api/protected_instance/kill"
        http_command = mcapi_url + \
                       mcapi + \
                       '?' + \
                       '&' + 'uuid=' + uuid + \
                       '&' + 'remote_uuid=' + remote_uuid + \
                       '&' + 'apikey=' + apikey
        request = requests.get(http_command)
        if request.status_code == 200:
            qq_message_send(qqapi_url, group_id, "发送成功！")
        elif request.status_code == 400:
            qq_message_send(qqapi_url, group_id, "发送失败，请求参数不正确，请检查配置文件。")
        elif request.status_code == 403:
            qq_message_send(qqapi_url, group_id, "发送失败，权限不够，请检查配置文件。")
        elif request.status_code == 404:
            qq_message_send(qqapi_url, group_id, "未找到后台API，请检查配置文件。")
        elif request.status_code == 500:
            qq_message_send(qqapi_url, group_id, "发送失败，可能是命令正在执行或是后台出现错误。")
        else:
            qq_message_send(qqapi_url, group_id, "发送失败，出现未知错误。")
    elif command == 'restart':
        mcapi = "/api/protected_instance/restart"
        http_command = mcapi_url + \
                       mcapi + \
                       '?' + \
                       '&' + 'uuid=' + uuid + \
                       '&' + 'remote_uuid=' + remote_uuid + \
                       '&' + 'apikey=' + apikey
        request = requests.get(http_command)
        if request.status_code == 200:
            qq_message_send(qqapi_url, group_id, "发送成功！")
        elif request.status_code == 400:
            qq_message_send(qqapi_url, group_id, "发送失败，请求参数不正确，请检查配置文件。")
        elif request.status_code == 403:
            qq_message_send(qqapi_url, group_id, "发送失败，权限不够，请检查配置文件。")
        elif request.status_code == 404:
            qq_message_send(qqapi_url, group_id, "未找到后台API，请检查配置文件。")
        elif request.status_code == 500:
            qq_message_send(qqapi_url, group_id, "发送失败，可能是命令正在执行或是后台出现错误。")
        else:
            qq_message_send(qqapi_url, group_id, "发送失败，出现未知错误。")
    else:
        mcapi = "/api/protected_instance/command"
        http_command = mcapi_url + \
                       mcapi + \
                       '?' + \
                       '&' + 'uuid=' + uuid + \
                       '&' + 'remote_uuid=' + remote_uuid + \
                       '&' + 'apikey=' + apikey + \
                       '&' + 'command=' + command
        # 用GET形式访问http_command，从而把我们的命令输进服务器
        request = requests.get(http_command)
        # 将此时的状态返回为request，便于检查和调试
        if request.status_code == 200:
            qq_message_send(qqapi_url, group_id, "发送成功！")
        elif request.status_code == 400:
            qq_message_send(qqapi_url, group_id, "发送失败，请求参数不正确，请检查配置文件。")
        elif request.status_code == 403:
            qq_message_send(qqapi_url, group_id, "发送失败，权限不够，请检查配置文件。")
        elif request.status_code == 404:
            qq_message_send(qqapi_url, group_id, "未找到后台API，请检查配置文件。")
        elif request.status_code == 500:
            qq_message_send(qqapi_url, group_id, "发送失败，可能是命令正在执行或是后台出现错误。")
        else:
            qq_message_send(qqapi_url, group_id, "发送失败，出现未知错误。")
    return request


def cq_processing(message):
    # 将表情所对应的CQ码转换为"表情"
    CQFaceID = 0
    while CQFaceID < 222:
        if ("[CQ:face,id=" + str(CQFaceID) + "]") in message:
            message = message.replace("[CQ:face,id=" + str(CQFaceID) + "]", "【表情】")
        CQFaceID += 1

    # 将语音所对应的CQ码转换为"语音"
    if message[0:11] == "[CQ:record,":
        message = "【语音】"

    # 将图片所对应的CQ码转换为"图片"
    if "[CQ:image," in message:
        if message[0:10] == "[CQ:image,":
            message = "【图片】"
        else:
            message = message.split("[CQ:image,")[0] + "【图片】"
    # 将回复类型的消息进行转换
    if "[CQ:reply,id=" in message:
        raw_message = (((message.split("[CQ:reply,id="))[1]).split('[CQ:at,qq='))[2].split('] ')[1]
        qqid = (((message.split("[CQ:reply,id="))[1]).split('[CQ:at,qq='))[2].split('] ')[0]
        mcid = QQMCBind.look_for_mcid(qqid)
        message = "【回复@" + str(mcid) + "】:" + str(raw_message)
    if "[CQ:at,qq=" in message:
        at_qqid = ((message.split("[CQ:at,qq="))[1].split('] '))[0]
        raw_message = ((message.split("[CQ:at,qq="))[1].split('] '))[1]
        mcid = QQMCBind.look_for_mcid(at_qqid)
        message = "@" + str(mcid) + " " + str(raw_message)
    return message


# 借助上一个发送命令的函数，同样可以定义出消息发送的函数
def mc_message_send(mcapi_url, uuid, remote_uuid, apikey, message, sender):
    mcapi = "/api/protected_instance/command"
    # 将我们手头上的消息进行第一步处理
    message = cq_processing(message)
    # 将前面已经处理好的消息进行第二步处理，变成一会会在游戏内看到的消息格式
    message_will_be_send = '*<' + sender + '> ' + message

    # 同样是运用字符串的拼接，将我们处理好的消息再次处理为JSON格式，并在最前面加上tellraw从而使其由服务端内部命令tellraw处理
    arg = "tellraw " + "@a " + "{\"text\":\"" + message_will_be_send + "\",\"color\":\"yellow\"}"
    # 将上一个处理好的字符串以命令的形式发送回服务器，从而实现与服务器之间的通信
    http_command = mcapi_url + \
                   mcapi + \
                   '?' + \
                   '&' + 'uuid=' + uuid + \
                   '&' + 'remote_uuid=' + remote_uuid + \
                   '&' + 'apikey=' + apikey + \
                   '&' + 'command=' + arg
    request = requests.get(http_command)
    return [request, message_will_be_send]
