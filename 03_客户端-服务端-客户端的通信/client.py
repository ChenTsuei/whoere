# -*- coding: utf-8 -*-

import socket
import threading

HOST = "127.0.0.1"
PORT = 23333
username = ""
is_normal = True

def recieve_msg(username, s):
    s.send(('login|%s' % username).encode('utf-8'))
    while True:
        data = s.recv(1024)
        print(data.decode('utf-8'))

username = input('Please input your name: ')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
t = threading.Thread(target=recieve_msg, args=(username, s))
t.start()

while is_normal:
    msg = input()
    if not msg: continue;
    if msg == 'exit':
        s.send(b'exit')
        break
    s.send(('say|%s' % msg).encode('utf-8'))