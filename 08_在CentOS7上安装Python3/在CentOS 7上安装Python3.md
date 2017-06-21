# 在CentOS 7上安装Python3

CentOS 7上默认只有Python 2，Python2虽然支持比较广泛，但是Python3是趋势，我们的开发也是选用的Python3，所以需要在CentOS系统的VPS上安装Python3。

## 步骤

### ssh连接远端主机

直接`ssh -p <端口号> <用户名>@<主机地址>`输入密码登录即可。

### 从官网下载Python最新版源码包并解压

下载：

```bash
wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1rc1.tgz
```

解压：

```bash
tar xf Python-3.6.1rc1.tgz ./
```

但是我在实际操作中发现这样解压会出现错误，换用绝对路径就好了。

```bash
tar xf Python-3.6.1rc1.tgz -C <路径>
```

### 编译安装

进入解压后的目录后，还是那熟悉的三步，不过第三步需要有些许变化，因为系统中自带Python 2，直接覆盖安装的话很多依赖于Python2的系统工具都会出现问题。

```bash
sudo ./configure --prefix=/usr/local
sudo make
sudo make altinstall
```

我在实际进行编译的时候发现系统中什么也没有，甚至连gcc这种东西都没有，所以要先用yum安装一下开发工具包。

```bash
yum groupinstall "Development tools"
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-develtk-devel gdbm-devel db4-devel libpcap-devel xz-devel
```

这样输入`python3.6`就可以运行了。
