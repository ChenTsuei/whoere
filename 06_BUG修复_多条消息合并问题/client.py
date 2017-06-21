# -*- coding: utf-8 -*-

import time
import socket
import threading

HOST = "127.0.0.1"
PORT = 23333
username = ""

# global variable
is_normal = True

def valid_username(username):
    for c in username:
        if not (c.isalnum() or c == '_'):
            return False
    return True

def list_cmd():
    print('exit: 登出并退出')
    print('help: 打开帮助菜单')
    print('lsu: 列出当前在线的人')
    print('lst: 列出当前所有主题')
    print('ntpc <主题内容>: 创建一个主题')
    print('dtpc <主题序号>: 删除你创建的主题')
    print('ch <用户名> <聊天内容>: 向指定用户发送一条消息')

def recieve_msg(username, s):
    global is_normal
    while is_normal:
        data = s.recv(1024).decode('utf-8').split('|')
        if data[0] == 'lsu':
            print()
            for i in range(1, len(data), 2):
                print('%s(%s)' % (data[i], data[i + 1]))
        elif data[0] == 'lst':
            s.send('recv'.encode('utf-8'))
            print(data)
            for i in range(1, len(data)):
                length = int(data[i])
                topic = s.recv(length).decode('utf-8').split('|')
                print("\n%s. %s(%s) 创建于 %s" % (topic[0], topic[1], topic[2], topic[3]))
                print("----%s" % topic[4])
        elif data[0] == 'dtpc':
            print()
            if data[1] == 'success':
                print('删除成功')
            else:
                print('删除失败')
        elif data[0] == 'send':
            if data[1] == 'fail':
                print('\n发送失败')
        elif data[0] == 'ch':
            print('\n[%s]: %s' % (data[1], data[2]))
    else: s.close()

def handle_msg(msg, s):
    global is_normal
    msg = msg.split()
    if msg[0] == 'exit':
        s.send('exit'.encode('utf-8'))
        is_normal = False
    elif msg[0] == 'help':
        if len(msg) > 1:
            print('参数过多')
        else:
            list_cmd()
    elif msg[0] == 'lsu' or msg[0] == 'lst':
        if len(msg) == 1:
            s.send(msg[0].encode('utf-8'))
        else:
            print('参数过多')
    elif msg[0] == 'ntpc':
        if len(msg) == 1:
            print('参数过少')
        else:
            temp_str = ' '.join(msg[1:])
            s.send(('ntpc|%s' % temp_str).encode('utf-8'))
    elif msg[0] == 'dtpc':
        if len(msg) < 2:
            print('参数过少')
        elif len(msg) > 2:
            print('参数过多')
        else:
            s.send(('dtpc|%s' % msg[1]).encode('utf-8'))
    elif msg[0] == 'ch':
        if len(msg) < 3:
            print('参数过少')
        else:
            temp_str = ' '.join(msg[2:])
            s.send(('ch|%s|%s' % (msg[1], temp_str)).encode('utf-8'))
    else:
        print('找不到此命令，请键入help打开帮助菜单')


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
except:
    print('与服务端连接失败')
    exit()

while True:
    username = input('请输入你的用户名:')
    if not username: continue
    if not valid_username(username):
        print('用户名不能包含特殊字符')
        continue
    s.send(('login|%s' % username).encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    if data == 'UserExist':
        print('用户名已存在')
        continue
    elif data == 'LoginSuccess':
        print('登录成功')
        break

data = s.recv(1024).decode('utf-8').split('|')
if data[0] == 'Status':
    print('在线人数: %s' % data[1])
    print('主题数: %s' % data[2])
list_cmd()

t = threading.Thread(target=recieve_msg, args=(username, s))
t.start()

while is_normal:
    msg = input('%s>' % username)
    if not msg: continue
    handle_msg(msg, s)