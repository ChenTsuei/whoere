# -*- coding: utf-8 -*-
import socket
import threading

HOST = "127.0.0.1"
PORT = 23333

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('Welcome!'.encode('utf-8'))
    data = sock.recv(1024)
    sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT)) 
s.listen(5) # 监听端口
print('Waiting for connection...')
while True:
    sock, addr = s.accept() # 接受一个新连接:
    t = threading.Thread(target=tcplink, args=(sock, addr)) # 创建新线程来处理TCP连接:
    t.start()