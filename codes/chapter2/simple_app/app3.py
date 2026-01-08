#2.3.3.2 HTTP的POST接口实现

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


#   设置路由为my_post，方法为POST
@app.route('/my_post', methods=['POST'])
def my_post():
    # 通过request.json接收前端以POST形式请求的内容
    get_data = request.json
    return f"接收到请求数据，内容为:{get_data}"


if __name__=='__main__':
        app.run()
