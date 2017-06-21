# -*- coding: utf-8 -*-
import time
import User
import socket
import threading

HOST = "127.0.0.1"
PORT = 23333

userlist = []

def hand_user_con(usr):
    while True:
        data = usr.skt.recv(1024).decode('utf-8')
        print(data)
        time.sleep(1)
        msg = data.split('|')
        if msg[0] == 'login':
            print('user [%s] login' % msg[1])
            usr.username = msg[1]
            usr.send_msg('Login Successfully')
        elif msg[0] == 'say':
            for user in userlist:
                if user != usr:
                    user.send_msg(usr.username + ' : ' + msg[1])
        elif msg[0] == 'exit':
            print('user [%s] exit' % usr.username)
            usr.logout()
            userlist.remove(usr)
            break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) 
s.listen(5) # 监听端口
print('Waiting for connection...')
while True:
    sock, addr = s.accept() # 接受一个新连接
    usr = User.User(sock)
    userlist.append(usr)
    t = threading.Thread(target=hand_user_con, args=(usr, )) # 创建新线程来处理TCP连接
    t.start()
s.close()
