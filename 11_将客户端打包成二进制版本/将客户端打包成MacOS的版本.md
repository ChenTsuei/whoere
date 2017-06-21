# 将客户端打包成二进制版本

决定使用[PyInstaller](http://www.pyinstaller.org/)工具进行打包，其[文档地址](https://pyinstaller.readthedocs.io/en/stable/)。

## MacOS版本的打包

用pip下载安装PyInstaller:

```bash
pip3 install PyInstaller
```

更改到*client.py*所在的目录，执行:

```bash
pyinstaller --onefile client.py
```

UNIX的可执行文件就是`./dist/client`

这里有个小插曲是`exit()`在打包之后不能正常使用，所以就将其更换为了`sys.exit(0)`。

## Windows版本的打包

我没有Windows系统又自己一个人在图书馆，所以干脆下个镜像装虚拟机……

安装出错，回去用舍友的电脑，发现是Python3.6版本太高PyInstaller不支持……

又换了一个舍友的电脑，正好是Python3.5，和MacOS下的命令相同，打包出一个*client.exe*来……

---

MacOS版的*client*，Win版的*client.exe*都在本目录下。
