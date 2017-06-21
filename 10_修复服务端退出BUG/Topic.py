# -*- coding: utf-8 -*-

import time

class Topic:
    def __init__(self, id, user, content):
        self.id = id
        self.user = user
        self.content = content
        self.date = time.strftime("%m-%d %H:%M:%S", time.localtime()) 
        