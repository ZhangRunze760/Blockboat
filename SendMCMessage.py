import yaml
import SendMessage
import re
import QQMCBind

with open('config.yaml', 'r', encoding='utf-8') as file:
    yaml_info = yaml.load(file, Loader=yaml.FullLoader)

MC = yaml_info['MC']
QQ = yaml_info['QQ']

QQAPI = QQ['QQAPI']
QQGroup_id = QQ['QQGroup_id']
log = MC['MCLOG']

death_pat = re.compile(r'([\d\D]*) (was|experienced|blew|hit|fell|went|walked|burned|trie|discovered|froze|starved'
                       r'|died|drowned|suffocated|withered)([\d\D]*)\n')
message_bak = None


# 定义MC消息获取函数，通过读取日志最后一行的形式获取消息
def lastline_get(fname):
    with open(fname, 'rb') as f:  # 打开文件
        off = -50  # 设置偏移量
        while True:
            f.seek(off, 2)  # seek(off, 2)表示文件指针：从文件末尾(2)开始向前50个字符(-50)
            lines = f.readlines()  # 读取文件指针范围内所有行
            if len(lines) >= 2:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
                last_line = lines[-1]  # 取最后一行
                break
            # 如果off为50时得到的readlines只有一行内容，那么不能保证最后一行是完整的
            # 所以off翻倍重新运行，直到readlines不止一行
            off *= 2
    # 这里需要注意，第一是读取出来的last_line是bytes形式，需要转换，第二是一定要用utf8编码，否则会出现乱码
    last_line = str(last_line, 'utf8')
    return last_line



def mc_message_processing(last_line):
    Message = ''
    # 分情况处理消息，返回处理好的消息内容
    if "[Server thread/INFO]" in last_line:
        if "[Server thread/INFO]: [Not Secure]" in last_line:
            Message = last_line[46:-1]
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

        # 用正则表达式处理死亡消息
        death_match = re.match(death_pat, last_line)
        if death_match is not None:
            Message = death_match
    if '@' in Message:
        mcid = (Message.split('@')[1]).split(' ')[0]
        qqid = QQMCBind.look_for_qqid(mcid)
        at = '@' + str(mcid) + ' '
        message_new = Message.replace(at, '[CQ:at,qq=' + str(qqid) + ']')
        return message_new
    else:
        return Message


# 通过一个死循环来反复读取日志最后一行，实现类似tail -f的功能
while True:
    message = mc_message_processing(lastline_get(log))
    # 比较这一次的读取和上一次的读取有什么不同，若相同，则不输出，反之则输出
    if message != message_bak and message is not None and message != 'None':
        # 将API返回的状态码和处理好的消息打印出来，便于检查与调试
        print(SendMessage.qq_message_send(QQAPI, QQGroup_id, message))
        print(message)
        message_bak = message
