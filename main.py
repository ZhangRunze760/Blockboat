import yaml
import QQMessageProcessing
from flask import Flask, request
import QQMCBind

# 运用with语句和yaml处理函数提取出我们在yaml文件中所写的数据，并打包为字典
with open('botconfig.yaml', 'r', encoding='utf-8') as file:
    yaml_info = yaml.load(file, Loader=yaml.FullLoader)
# 将这部字典中的两部字典提取出来
QQ = yaml_info['QQ']
MC = yaml_info['MC']
# 再将这两部字典中的数据提取出来，供我们后面调用
QQAPI = QQ['QQAPI']
QQGroup_id = QQ['QQGroup_id']
QQPort = QQ['QQPort']
QQURL = QQ['QQURL']

MCURL = MC['MCURL']
MCUUID = MC['MCUUID']
MCREMOTE_UUID = MC['MCREMOTE_UUID']
MCAPIKEY = MC['MCAPIKEY']
java_edition = MC['IsJavaEdition']
app = Flask(__name__)


@app.route('/', methods=["POST"])
def post_data():
    # 将得到的数据打印，便于检查与调试
    print(request.get_json())

    if request.get_json().get('group_id') == QQGroup_id:
        with open('Bind.yaml', 'r', encoding='utf-8') as yaml_file:
            bind_info = yaml.load(yaml_file, Loader=yaml.FullLoader)
            list_of_qqid = list(bind_info.keys())

        # 获取需要的消息
        qqid = request.get_json().get('sender').get('user_id')  # 发送者的QQ号
        if str(qqid) in list_of_qqid:
            who = QQMCBind.look_for_mcid(qqid)
        else:
            who = request.get_json().get('sender').get('card')
        message = request.get_json().get('raw_message')  # 发的什么东西

        QQMessageProcessing.qq_message_processing(QQAPI, QQGroup_id, MCURL, MCUUID, MCREMOTE_UUID, MCAPIKEY, message,
                                                  qqid, who, java_edition)

    return 'OK'  # 对go-cqhttp进行响应，不然会出现三次重试


# 开启我们的端口监听，监听我们设置好的端口，从而使得机器人框架向我们上报消息
app.run(debug=True, host=QQURL, port=int(QQPort))
