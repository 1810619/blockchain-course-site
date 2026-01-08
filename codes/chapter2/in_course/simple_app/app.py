# -*- coding: utf-8 -*-
# File : app.py.py
# Author: taoyahui
# Date : 2022/9/6
from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/my_get', methods=['GET'])
def my_get():
    """

    :return:
    """
    arg1 = request.args.get("arg1")
    arg2 = request.args.get("arg2")
    return f"接收到参数，分别为: arg1: {arg1} , arg2: {arg2}"


@app.route('/my_post', methods=['POST'])
def my_post():
    # 通过request.json接收前端以POST形式请求的内容
    get_data = request.json
    return f"接收到请求数据，内容为:{get_data}"

if __name__ == '__main__':
    app.run()


