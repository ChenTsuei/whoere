# -*- coding: utf-8 -*-
import socket

HOST = "127.0.0.1"
PORT = 23333

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(s.recv(1024).decode('utf-8'))
nick = input()
s.send(nick.encode('utf-8'))
print(s.recv(1024).decode('utf-8'))