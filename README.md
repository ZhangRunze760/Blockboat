#qqbot命令列表
 直接输入即可

  #sudo list        相当于原版的/list命令，返回这个命令的输出
   sudo + <命令>    需要权限的命令，如果有权限，则直接通过API输入进控制台  例如<whitelist add><whitelist list>...
   bind + <MCID>    绑定命令，将QQ号与MCID进行绑定，便于QQ与服务器通信
   unbind           解绑命令，不需要任何参数


   sudo bindcontrol 需要权限的绑定机制控制命令，有四种形式：
      sudo bindcontrol add + <@某人> + <MCID>  将某人的QQ号与mcid绑定，第一个参数用@某人或某人的QQ号均可，第二个参数一定得是这个人的mcid
      sudo bindcontrol remove-qqid + <@某人>   将某人的QQ号与mcid解绑，参数用@某人或某人的QQ号均可，作用效果与这个人执行unbind一致
      sudo bindcontrol remove-mcid + <MCID>    将某人的mcid与QQ号解绑，参数一定得是这个人的mcid，作用效果与这个人执行unbind一致
      sudo bindcontrol list                    返回所有绑定过的QQ号与mcid列表