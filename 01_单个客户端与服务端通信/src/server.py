# -*- coding: utf-8 -*-
import socket

HOST = "127.0.0.1"
PORT = 23333

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) 
s.listen(1) # 监听端口
print('Waiting for connection...')
sock, addr = s.accept() # 接受一个新连接
sock.send('Welcome!'.encode('utf-8'))
data = sock.recv(1024)
sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
sock.close()
print('Connection from %s:%s closed.' % addr)