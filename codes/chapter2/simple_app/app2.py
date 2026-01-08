#2.3.3.1  HTTP的GET接口的实现

from flask import Flask
from flask import request  # 引入此依赖，可以接收HTTP请求信息
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/my_get', methods=['GET'])
def my_get():
    arg1 = request.args.get("arg1")  # 使用request.args可以接收GET请求的参数
    arg2 = request.args.get("arg2")
    return f"接收到参数，分别为: arg1: {arg1} , arg2: {arg2}"  # HTTP请求对应的相应

if __name__=='__main__':
        app.run()
