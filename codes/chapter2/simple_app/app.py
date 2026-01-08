from flask import Flask
from flask import request  # 引入此依赖，可以接收HTTP请求信息
import services

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


@app.route('/encrypt', methods=['GET'])
def encrypt():
    """
    哈希函数加密
    :return: 加密的字典对象
    """
    data = request.args.get('data')
    res = services.hash_encrypt(data)
    return {
        'res': res
    }


if __name__ == '__main__':
    app.run()
