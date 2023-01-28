import QQMCBind
import SendMessage


def cq_processing(message):
    message = str(message)
    # 将表情所对应的CQ码转换为"表情"
    if "[CQ:face," in message and "]" in message:
        CQ_code = '[' + message.split('[')[1].split(']')[0] + ']'
        message = message.replace(CQ_code, "【表情】")

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


# 定义我们的权限识别函数，通过访问oplist.txt来识别member的权限
def is_member_in_oplist(member):
    filename = "oplist.txt"
    oplist = open(filename, mode="r")
    # 提取出文本中的字符串
    text = str(oplist.read())
    oplist.close()
    # 判断所提供的QQ号是否为字符串的一部分
    if str(member) in text:
        return True
    else:
        return False


# 定义QQ消息的处理并检查是否为命令，同时调用SendMessage中的命令发送函数执行它，若不是，则作为消息进行转发
def qq_message_processing(qqapi_url, qqgroup_id, mcapi_url, uuid, remote_uuid, apikey, message, qqid, sender,
                          java_edition):
    warning = "权限不够！"
    message = str(message)
    # 判断命令是否为无需权限即可执行的list
    if message == "sudo list":
        return SendMessage.mc_command_send(qqapi_url, qqgroup_id, mcapi_url, uuid, remote_uuid, apikey, 'list')

    # 判断是否为绑定，若是，则运行QQMCBind库中的绑定函数写入yaml文件
    elif message[0:5] == "bind ":
        arg = message.split(" ")[-1]
        QQMCBind.qq_bind_with_mc(qqapi_url, qqgroup_id, qqid, arg)
    elif message == "unbind":
        QQMCBind.qq_mc_unbind(qqapi_url, qqgroup_id, str(qqid))

    # 判断消息前四位是否为命令前缀sudo，如果是，则按命令的形式处理
    elif message[0:5] == "sudo ":
        # 调用前面定义的权限识别函数，识别用户的权限
        if is_member_in_oplist(qqid):
            command = message.replace("sudo ", "")

            if command[0:12] == "bindcontrol ":
                args = command.replace("bindcontrol ", '')

                if args[0:4] == 'add ':
                    argc = args.split(' ')[1]
                    argv = args.split(' ')[2]
                    argc = (argc.replace('[CQ:at,qq=', '')).replace(']', '')
                    return QQMCBind.qq_bind_with_mc(qqapi_url, qqgroup_id, argc, argv)

                elif args[0:12] == 'remove-qqid ':
                    arg = ((args.split("[CQ:at,qq="))[1].split('] '))[0]
                    return QQMCBind.qq_mc_unbind(qqapi_url, qqgroup_id, arg)

                elif args[0:12] == 'remove-mcid ':
                    arg = QQMCBind.look_for_qqid(args.split(' ')[1])
                    return QQMCBind.qq_mc_unbind(qqapi_url, qqgroup_id, arg)

                elif args[0:4] == 'list':
                    bind_file = open('Bind.yaml', 'r', encoding='utf-8')
                    lines = ''
                    for string in bind_file:
                        lines += string
                    return SendMessage.qq_message_send(qqapi_url, qqgroup_id, lines)

            else:
                return SendMessage.mc_command_send(qqapi_url, qqgroup_id, mcapi_url, uuid, remote_uuid, apikey, command)
            return SendMessage.mc_command_send(qqapi_url, qqgroup_id, mcapi_url, uuid, remote_uuid, apikey, command)
        else:
            return SendMessage.qq_message_send(qqapi_url, qqgroup_id, warning)


    # 如果没有上述前缀，则视为普通消息进行转发
    else:
        return SendMessage.mc_message_send(mcapi_url, uuid, remote_uuid, apikey, message, sender, java_edition)


def qq_command_processing(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey, message, edition):
    mc_command_body = message.replace("!!", '')
    mc_command_arg = mc_command_body.split(' ')[0]
    if mc_command_arg == 'shut':
        arg = QQMCBind.look_for_qqid(mc_command_body.split(' ')[1])
        time = mc_command_body.split(' ')[2]
        request = SendMessage.qq_shut_send(qqapi_url, qqgroup_id, arg, time)
    elif mc_command_arg == 'shutall':
        enable = bool(mc_command_body.split(' ')[1])
        request = SendMessage.qq_shutall_send(qqapi_url, qqgroup_id, enable)
    elif mc_command_arg == 'kick':
        qqid = QQMCBind.look_for_qqid(mc_command_body.split(' ')[1])
        request = SendMessage.qq_kick_send(qqapi_url, qqgroup_id, qqid)
    else:
        SendMessage.send_robot_message(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey, "输入错误！",
                                       edition)
        request = None
    if request.status_code == 200:
        SendMessage.send_robot_message(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey, "发送成功！",
                                       edition)
    elif request.status_code == 400:
        SendMessage.send_robot_message(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey,
                                       "发送失败，请求参数不正确，请检查配置文件。",
                                       edition)
    elif request.status_code == 403:
        SendMessage.send_robot_message(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey,
                                       "发送失败，权限不够，请检查配置文件。",
                                       edition)
    elif request.status_code == 404:
        SendMessage.send_robot_message(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey,
                                       "发送失败，未找到后台API，请检查配置文件。",
                                       edition)
    elif request.status_code == 500:
        SendMessage.send_robot_message(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey,
                                       "发送失败，可能是命令正在执行或后台出现错误。",
                                       edition)
    else:
        SendMessage.send_robot_message(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey,
                                       "发送失败，出现未知错误。",
                                       edition)


def mc_message_processing(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey, edition, last_line):
    Message = ''
    # 分情况处理消息，返回处理好的消息内容
    if "[Server thread/INFO]" in last_line:
        if "[Server thread/INFO]: [Not Secure]" in last_line:
            Message = last_line[46:-1]
            raw_message = Message.replace('<', '').split('> ')[1]
            sender = QQMCBind.look_for_qqid(Message.replace('<', '').split('> ')[0])
            if raw_message[0:2] == "!!":
                if is_member_in_oplist(sender):
                    qq_command_processing(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey,
                                          raw_message, edition)
                    return None
                else:
                    SendMessage.send_robot_message(qqapi_url, qqgroup_id, mcapi_url, mcuuid, mcremote_uuid, mcapikey,
                                                   '权限不够！', edition)
                    return None

        if "[Server thread/INFO]: There are" in last_line:
            Message = last_line[33:-1]
        if "[pool-2-thread-1/INFO]: [Textile Backup] Starting backup" in last_line:
            Message = "开始备份...可能会出现微小卡顿。"
        if "[pool-2-thread-1/INFO]: [Textile Backup] Compression took:" in last_line:
            Message = "备份完成！花费时间：" + last_line[58:-1]
        if "[Server thread/INFO]" in last_line and " joined the game" in last_line:
            Message = last_line[33:-17] + "加入了游戏"
        if "[Server thread/INFO]" in last_line and "left the game" in last_line:
            Message = last_line[33:-15] + "退出了游戏"
    else:
        if "[pool-2-thread-1/INFO]: [Textile Backup] Starting backup" in last_line:
            Message = "开始备份...可能会出现微小卡顿。"
        if "[pool-2-thread-1/INFO]: [Textile Backup] Compression took:" in last_line:
            Message = "备份完成！花费时间：" + last_line[70:-1]

    if '@' in Message:
        mcid = (Message.split('@')[1]).split(' ')[0]
        qqid = QQMCBind.look_for_qqid(mcid)
        at = '@' + str(mcid) + ' '
        message_new = Message.replace(at, '[CQ:at,qq=' + str(qqid) + ']')
        return message_new
    else:
        return Message
