# -*- coding: utf-8 -*-
# File : demo_server.py
# Author: taoyahui
# Date : 2022/3/30

from flask import Flask,request #导入Flask类(创建Flask应用)和request对象(处理HTTP请求)
import flask_socketio    #导入flask_socketio模块
app = Flask(__name__)    #创建一个Flask应用实例，__name__作为参数，赋值给app变量

'''#定义变量名为my_socketio防止重名
#创建一个Socket.IO服务器实例，并将其绑定到Flask应用实例app上。
#cors_allowed_origins='*' 配置内容允许所有来源的跨域请求'''
my_socketio = flask_socketio.SocketIO(app, cors_allowed_origins='*')


@my_socketio.on('message')            #使用装饰器创建以"message"为标识的socket接口
def message(message):                       
    print(f"receive message : {message}")   #打印接收到的消息内容


if __name__ == '__main__':     #确保以下代码只在直接运行脚本时执行，而在作为模块导入时不执行
    # 启动Flask应用；如下host表示在所有可用的IP地址（0.0.0.0）的端口5000上监听
    # debug=True开启调试模式
    my_socketio.run(app, host='0.0.0.0', port=5000, debug=True)
