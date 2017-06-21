# 用screen命令让服务端在后台运行

在使用ssh或者telnet登录远程主机后，执行一些耗时的命令，如果此时ssh或者telnet中断，那么远程主机上正在执行的程序或者说命令也会被迫终止。screen能够很好地解决这个问题。screen也叫*虚拟终端*，可以在一个物理终端上实现多个虚拟终端的效果。

这里来说一下常规用法：

1、新建一个`screen`

直接`screen`或者`screen -S XXX`（XXX是你为这个screen指定的名字）

2、在`screen`中新建一个虚拟终端（此时你的screen中就有了两个虚拟终端了）

`Ctrl + A + C`（先按`Ctrl + A`，然后再按`C`，下面的命令也一样）

3、在虚拟终端之间切换

前一个`Ctrl + A + P`

后一个`Ctrl + A + N`

4、关闭一个虚拟终端

`Ctrl + A + K`或者`exit`

5、挂起screen（挂起之后你又回到了创建screen的shell）

`Ctrl + A + D`

6、重新连接screen

`screen -ls`列出当前挂起的screen

比如有这样一条“8888.XXX (Detached)”

那么可以使用`screen -r 8888`或者`screen -r XXX`来重新连接。