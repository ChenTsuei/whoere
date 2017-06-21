# -*- coding: utf-8 -*-
import time
import User
import Topic
import socket
import threading

HOST = "127.0.0.1"
PORT = 23333

# global variable
is_normal = True
userlist = []
topiclist = []
topicid = 0

def hand_user_con(usr):
    global is_normal, topicid, userlist, topiclist
    while True:
        data = usr.skt.recv(1024).decode('utf-8').split('|')
        exist = False
        for user in userlist:
            if data[1] == user.username:
                usr.send_msg('UserExist')
                exist = True
                break
        if exist: continue
        else:
            usr.send_msg('LoginSuccess')
            break
    usr.username = data[1]
    userlist.append(usr)
    usr.send_msg('Status|%d|' % len(userlist) + str(len(topiclist)))
    while True:
        data = usr.skt.recv(1024).decode('utf-8')
        time.sleep(1)
        print(usr.username, data)
        msg = data.split('|')
        if msg[0] == 'exit':
            usr.logout()
            userlist.remove(usr)
            break
        elif msg[0] == 'lsu':
            send_data = ['lsu']
            for user in userlist:
                send_data.append(user.username)
                send_data.append(user.addr)
            usr.send_msg('|'.join(send_data))
        elif msg[0] == 'lst':
            for topic in topiclist:
                usr.send_msg('lst|%s|%s|%s|%s|%s|' % (str(topic.id), 
                    topic.user.username, topic.user.addr, topic.date, topic.content))
        elif msg[0] == 'ntpc':
            topicid += 1
            topic = Topic.Topic(topicid, usr, msg[1])
            topiclist.append(topic)
        elif msg[0] == 'dtpc':
            tid = int(msg[1])
            success = False
            for topic in topiclist:
                if tid == topic.id and usr.username == topic.user.username:
                    success = True
                    break
            if success:
                topiclist.remove(topic)
                usr.send_msg('dtpc|success')
            else:
                usr.send_msg('dtpc|fail')
        elif msg[0] == 'ch':
            success = False
            for user in userlist:
                if user.username == msg[1]:
                    success = True
                    user.send_msg('ch|%s|%s' % (usr.username, msg[2]))
            if success:
                usr.send_msg('send|success')
            else:
                usr.send_msg('send|fail')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) 
s.listen(5) # 监听端口
print('Waiting for connection...')
while is_normal:
    sock, addr = s.accept() # 接受一个新连接
    usr = User.User(sock, addr[0])
    t = threading.Thread(target=hand_user_con, args=(usr, )) # 创建新线程来处理TCP连接
    t.start()
s.close()
