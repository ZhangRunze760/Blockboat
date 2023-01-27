import time

import yaml

import MessageProcessing
import SendMessage

with open('botconfig.yaml', 'r', encoding='utf-8') as file:
    yaml_info = yaml.load(file, Loader=yaml.FullLoader)

MC = yaml_info['MC']
QQ = yaml_info['QQ']

QQAPI = QQ['QQAPI']
QQGroup_id = QQ['QQGroup_id']
MCURL = MC['MCURL']
MCUUID = MC['MCUUID']
MCREMOTE_UUID = MC['MCREMOTE_UUID']
MCAPIKEY = MC['MCAPIKEY']
java_edition = MC['IsJavaEdition']
log = MC['MCLOG']
lastline_bak = None


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


# 通过一个死循环来反复读取日志最后一行，实现类似tail -f的功能
while True:
    lastline = lastline_get(log)
    message = MessageProcessing.mc_message_processing(QQAPI, QQGroup_id, MCURL, MCUUID, MCREMOTE_UUID, MCAPIKEY,
                                                      java_edition, lastline)
    # 比较这一次的读取和上一次的读取有什么不同，若相同，则不输出，反之则输出
    if lastline != lastline_bak and message is not None and message != 'None':
        # 将API返回的状态码和处理好的消息打印出来，便于检查与调试
        print(SendMessage.qq_message_send(QQAPI, QQGroup_id, message))
        print(message)
        lastline_bak = lastline
        time.sleep(0.3)
