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

def new_sock(s):
    global is_normal
    while is_normal:
        try:
            sock, addr = s.accept() # 接受一个新连接
        except:
            break
        usr = User.User(sock, addr[0])
        t = threading.Thread(target=hand_user_con, args=(usr, )) # 创建新线程来处理TCP连接
        t.start()

def hand_login(usr):
    global userlist, topiclist
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
    print('\n%s|login' % usr.username)
    usr.send_msg('Status|%d|' % len(userlist) + str(len(topiclist)))

def hand_lsu(usr):
    global userlist
    send_data = ['lsu']
    for user in userlist:
        send_data.append(user.username)
        send_data.append(user.addr)
    usr.send_msg('|'.join(send_data))

def hand_lst(usr):
    global topiclist
    if topiclist != []:
        send_datas = []
        for topic in topiclist:
            send_datas.append('%s|%s|%s|%s|%s' % (str(topic.id), 
                topic.user.username, topic.user.addr, topic.date, topic.content))
        send_data_len = [str(len(x)) for x in send_datas]
        usr.send_msg('lst|' + ('|'.join(send_data_len)))
        data = usr.skt.recv(4).decode('utf-8')
        for send_data in send_datas:
            usr.send_msg(send_data)
    else:
        usr.send_msg('lst')

def hand_ntpc(usr, content):
    global topicid, topiclist
    topicid += 1
    topic = Topic.Topic(topicid, usr, content)
    topiclist.append(topic)

def hand_dtpc(usr, sid):
    global topiclist
    tid = int(sid)
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

def hand_ch(usr, username, content):
    global userlist
    success = False
    for user in userlist:
        if user.username == username:
            success = True
            user.send_msg('ch|%s|%s' % (usr.username, content))
    if success:
        usr.send_msg('send|success')
    else:
        usr.send_msg('send|fail')

def hand_user_con(usr):
    global is_normal, topicid, userlist, topiclist
    hand_login(usr)
    while is_normal:
        data = usr.skt.recv(1024).decode('utf-8')
        time.sleep(1)
        print()
        print(usr.username, '~', data)
        msg = data.split('|')
        if msg[0] == 'exit':
            usr.logout()
            userlist.remove(usr)
            break
        elif msg[0] == 'lsu':
            hand_lsu(usr)
        elif msg[0] == 'lst':
            hand_lst(usr)
        elif msg[0] == 'ntpc':
            hand_ntpc(usr, msg[1])
        elif msg[0] == 'dtpc':
            hand_dtpc(usr, msg[1])
        elif msg[0] == 'ch':
            hand_ch(usr, msg[1], msg[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) 
s.listen(5) # 监听端口
print('服务启动')
t = threading.Thread(target=new_sock, args=(s, ))
t.start()

while is_normal:
    msg = input('admin>')
    if not msg: continue
    if msg == 'lsu':
        print('\n在线人数: %s' % len(userlist))
        for user in userlist:
            print('%s(%s)' % (user.username, user.addr))
        print()
    elif msg == 'lst':
        print('\n主题个数: %s' % len(topiclist))
        for topic in topiclist:
            print("\n%d. %s(%s) 创建于 %s" % (topic.id, topic.user.username, 
                topic.user.addr, topic.date))
            print("----%s" % topic.content)
        print()
    elif msg == 'exit':
        is_normal = False
        for user in userlist:
            user.send_msg('exit')
        break
s.close()