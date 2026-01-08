# -*- coding: utf-8 -*-
# File : socket1.py
# Author: taoyahui
# Date : 2022/3/28

from flask import Flask,request   #导入Flask类和request对象
import flask_socketio             #导入flask_socketio模块
import socketio                   #导入socketio模块
app = Flask(__name__)             #创建一个Flask应用实例，赋值给app变量

# 创建Socket服务端。不要命名为socketio，这将与引用的依赖包重名！
my_socketio = flask_socketio.SocketIO(app, cors_allowed_origins='*')

@my_socketio.on('message')   #使用装饰器创建以"message"为标识的socket接口
def message(message):
    print(f"receive message : {message}")

#使用装饰器，客户端发起对路径/send的HTTP POST请求时，调用下面定义的函数send_message
@app.route('/send', methods=['POST'])
def send_message():
    # 从HTTP请求中获取JSON数据，并将其存储在变量body中
    body = request.json
    # 创建Socket客户端
    sio = socketio.Client()
    # 连接socket2的服务端，端口号为5001
    sio.connect('http://localhost:5001')
    # 发送数据
    sio.emit("message", body['data'])
    # 断开连接
    sio.disconnect()
    return "ok"

if __name__ == '__main__':         #代码在直接运行脚本时执行
    # 节点1(socket1)，配置端口为5000
    my_socketio.run(app, host='0.0.0.0', port=5000, debug=True)
