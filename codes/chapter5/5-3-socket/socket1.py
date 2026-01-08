from flask import Flask,request
import flask_socketio
import socketio
app = Flask(__name__)

# 创建Socket服务端。不要命名为socketio，这将与引用的依赖包重名
my_socketio = flask_socketio.SocketIO(app, cors_allowed_origins='*')

@my_socketio.on('message')
def message(message):
    print(f"receive message : {message}")

@app.route('/send', methods=['POST'])
def send_message():
    body = request.json
    # 创建Socket客户端
    sio = socketio.Client()
    # 连接socket2的服务端，端口号为5001
    sio.connect('http://192.168.2.23:5001')
    # 发送数据
    sio.emit("message", body['data'])
    # 断开连接
    sio.disconnect()
    return "ok"

if __name__ == '__main__':
    # 节点1（socket1），配置端口为5000
	my_socketio.run(app, host='0.0.0.0', port=5000, debug=True)
