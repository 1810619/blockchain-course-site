# -*- coding: utf-8 -*-
# File : demo_client.py
# Author: taoyahui
# Date : 2022/3/30

import socketio          #导入socketio模块
import time              #导入time模块
sio = socketio.Client() #创建Socket.IO客户端实例sio，实现客户端向服务端发送数据请求
sio.connect('http://localhost:5000') #建立客户端与服务端连接的通道

for i in range(0,10):
    sio.emit("message", 'hello, this is client')  #向服务端发送请求;名称、消息内容
    time.sleep(1)                                 #休眠1秒

sio.disconnect()
