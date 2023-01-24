import yaml
import SendMessage


# 先定义删除某一行的函数，以便于定义解绑函数
def remove_line(filename, lineno):
    fro = open(filename, "r", encoding='UTF-8')

    current_line = 0
    while current_line < lineno:
        fro.readline()
        current_line += 1

    seekpoint = fro.tell()
    frw = open(filename, "r+")
    frw.seek(seekpoint, 0)
    fro.readline()  # 读入一行进内存，同时文件指针下移实现删除
    chars = fro.readline()
    while chars:
        frw.writelines(chars)
        chars = fro.readline()

    fro.close()
    frw.truncate()
    frw.close()


# 通过QQ号来查询MCID
def look_for_mcid(qqid):
    with open('Bind.yaml', 'r', encoding='utf-8') as yaml_file:
        bind_info = yaml.load(yaml_file, Loader=yaml.FullLoader)
        mcid = bind_info[str(qqid)]
        return mcid


# 通过MCID来查询QQ号
def look_for_qqid(mcid):
    with open('Bind.yaml', 'r', encoding='utf-8') as yaml_list:
        bind_info = yaml.load(yaml_list, Loader=yaml.FullLoader)
    list_of_qqid = list(bind_info.keys())
    list_of_mcid = list(bind_info.values())
    position = list_of_mcid.index(mcid)
    qqid = list_of_qqid[position]
    return qqid


# 通过直接写入文件的方式，定义出绑定函数
def qq_bind_with_mc(qqapi_url, group_id, qqid, mcid):
    with open('Bind.yaml', 'r', encoding='utf-8') as yaml_list:
        bind_info = yaml.load(yaml_list, Loader=yaml.FullLoader)
    list_of_qqid = list(bind_info.keys())
    string = "\"" + str(qqid) + "\": \"" + str(mcid) + "\"" + "\n"
    if str(qqid) in list_of_qqid:
        SendMessage.qq_message_send(qqapi_url, group_id, "QQ号已绑定MCID，不支持一个QQ号绑定多个MCID")
        print("NO!")
    else:
        fileadd = open("Bind.yaml", "a")
        fileadd.writelines(string)
        SendMessage.qq_message_send(qqapi_url, group_id, "绑定成功！")


# 通过前面的删除行的函数，可以很轻松的定义出解绑函数
def qq_mc_unbind(qqapi_url, group_id, qqid):
    with open('Bind.yaml', 'r', encoding='utf-8') as yaml_list:
        bind_info = yaml.load(yaml_list, Loader=yaml.FullLoader)
    list_of_qqid = list(bind_info.keys())
    if qqid in list_of_qqid:
        position = list_of_qqid.index(qqid)
        remove_line('Bind.yaml', position)
        SendMessage.qq_message_send(qqapi_url, group_id, "解绑成功！")
    else:
        SendMessage.qq_message_send(qqapi_url, group_id, "未绑定任何MCID，无法解绑！")
