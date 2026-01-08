import models
import json

from flask import Flask, request
app = Flask(__name__)

blockchain = models.Blockchain()


@app.route('/add', methods=['POST'])
def add():
    """
    区块链添加功能API
    :return:
    """
    body = request.json
    index = blockchain.add_new_block(body['data'])
    return json.dumps({
        'code':200,
        'data':index
    })


@app.route('/query', methods=['GET'])
def query():
    index = int(request.args['index'])
    return json.dumps({
        'code': 200,
        'data': blockchain.query_block_info(index)
    })


if __name__ == '__main__':
    app.run()
