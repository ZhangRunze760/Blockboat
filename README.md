# 简介
Blockboat（百舸）QQ机器人，支持任何一种java版mc服务端的群服互联机器人，支持游戏内at，再也不怕冷群。
# 预备环境
MC服务端，go-cqhttp框架，MCSManager 9.x。
# 功能
群消息转发、游戏内消息转发、QQ号与MCID绑定、群内发送命令、管理员管理绑定机制、游戏内@已绑定QQ号的群员。

# 命令列表
    sudo list        相当于原版的/list命令，返回这个命令的输出
    sudo + <命令>    需要权限的命令，如果有权限，则直接通过API输入进控制台  例如<whitelist add><whitelist list>...
    bind + <MCID>    绑定命令，将发送者的QQ号与MCID进行绑定，便于QQ与服务器通信
    unbind           解绑命令，不需要任何参数，只能解绑发送者的绑定
    sudo bindcontrol 需要权限的绑定机制控制命令，有四种形式：
      sudo bindcontrol add + <@某人> + <MCID>  将某人的QQ号与mcid绑定，第一个参数用@某人或某人的QQ号均可，第二个参数一定得是这个人的mcid
      sudo bindcontrol remove-qqid + <@某人>   将某人的QQ号与mcid解绑，参数用@某人或某人的QQ号均可，作用效果与这个人执行unbind一致
      sudo bindcontrol remove-mcid + <MCID>    将某人的mcid与QQ号解绑，参数一定得是这个人的mcid，作用效果与这个人执行unbind一致
      sudo bindcontrol list                    返回所有绑定过的QQ号与mcid列表
# 安装教程
首先准备好预备环境，安装MCSManager。登录MCSManager面板，创建三个新的实例，分别对应QQ机器人框架（go-cqhttp）、QQ机器人本体、QQ机器人的MC消息转发模块。
其次，下载机器人并导入，将QQ机器人本体与MC的消息转发模块和go-cqhttp放在同一目录下，按照go-cqhttp的官方文档按http模式配置好。打开配置文件config.yml，拉到最下面，配置http post，打开go-cqhttp，检查配置（此时如果有post上报失败的消息，属于正常现象）。一切准备就绪以后，打开MCSManager，找到自己账户的APIKEY和实例的UID与GID，备用。打开机器人的配置文件botconfig.yaml，将数据按照自带的注释填进去。
最后，先打开自己的MC服务端，再打开机器人框架，最后打开机器人对应的两个程序，即可开始享受群服互通消息的快感了。
