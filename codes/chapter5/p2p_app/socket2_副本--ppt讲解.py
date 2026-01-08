# -*- coding: utf-8 -*-
# File : socket2.py
# Author: taoyahui
# Date : 2022/3/28


#引入相关依赖；  #创建一个Flask应用实例；   #创建Socket服务端 
#使用装饰器创建以"message"为标识的socket接口；  #定义message函数
#使用装饰器，客户端发起对路径/send的HTTP POST请求时，调用下面定义的函数send_message
@app.route('/send', methods=['POST'])
def send_message():
    body = request.json
    # 创建Socket客户端
    sio = socketio.Client()
    # 连接socket1的服务端，端口号为5000
    sio.connect('http://localhost:5000')
    sio.emit("message", body['data'])
    # 断开连接
    sio.disconnect()
    return "ok"

if __name__ == '__main__':       #代码在直接运行脚本时执行
    # 节点1(socket2)，配置端口为5001
    my_socketio.run(app, host='0.0.0.0', port=5001, debug=True)
