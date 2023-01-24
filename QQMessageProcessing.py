import SendMessage
import QQMCBind


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
def qq_message_processing(qqapi_url, qqgroup_id, mcapi_url, uuid, remote_uuid, apikey, message, qqid, sender):
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
        return SendMessage.mc_message_send(mcapi_url, uuid, remote_uuid, apikey, message, sender)
