# -*- coding: utf-8 -*-
import socket 

class User:
    def __init__(self, skt, addr, username='none'):
        self.skt = skt
        self.addr = addr
        self.username = username
    def send_msg(self, msg):
        self.skt.send(msg.encode('utf-8'))
    def logout(self):
        self.skt.close()