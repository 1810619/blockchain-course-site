# -*- coding: utf-8 -*-
# File : app0.py
# Author: taoyahui
# Date : 2022/4/1
from flask import Flask, request, jsonify
import flask_socketio
import p2p_services
import pow_services
import models
import entity
from flask_apscheduler import APScheduler
from datetime import datetime
import config
import crypto_util
import http_res

network = entity.network  # 获取区块链网络内容，根据实际节点情况切换
c_peer = entity.peer1  # 取出当前进程的节点内容，根据实际情况切换
http_port = 5001  # 定义HTTP使用端口

app = Flask(__name__)

# 创建socket客户端
scheduler = APScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True
app.config.from_object(Config())
scheduler.init_app(app)

@scheduler.task('interval',
                id='send_message',
                seconds=config.version_req_interval_seconds,
                misfire_grace_time=900)
def send_message():
    p2p_services.send_version(c_peer, network)

# 创建socket服务端处理内容
peer_socketio = flask_socketio.SocketIO(app, cors_allowed_origins='*')
@peer_socketio.on('peer-version')
def peer_version(rec_msg):
    p2p_services.peer_version_services(rec_msg, c_peer, c_peer.sio)

@peer_socketio.on('peer-message')
def peer_message(msg_dict):
    p2p_services.peer_message_service(msg_dict, c_peer)


#创建节点0(peer0)，进行PoW计算的任务
@scheduler.task('interval',
                id='peer-calc',
                seconds=config.pow_interval_seconds,
                misfire_grace_time=900)
def peer_exe_pow():
    # 设置统一的区块数据
    # data = f"{entity.peer0.name}-{datetime.now().strftime('%Y/%m/%d %H:%M:%S')}"
    if len(c_peer.pool) == 0:
        tx_content = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        tx = models.Transaction("0" * 32, "0" * 32, f"交易内容为: {tx_content}", datetime.now())
        tx.gen_id()
        tx.gen_sig(entity.d_pk)
        c_peer.pool.append(tx)
    pow_services.exe_pow(data=c_peer.pool, peer=c_peer)
    c_peer.pool = []


@app.route("/account_create", methods=['GET'])
def account_create():
    """
    创建账户接口
    :return:
    """
    return jsonify({
        'code': 200,
        'data': crypto_util.create_account()
    })


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """
    新增一笔交易
    :return:
    """
    body = request.json
    if 'sender' not in body or 'recipient' not in body or 'data' not in body or 'private_key' not in body:
        return jsonify(http_res.empty_res)
    new_transaction = models.Transaction(body['sender'], body['recipient'], body['data'], datetime.now())
    new_transaction.gen_id()
    new_transaction.gen_sig(body['private_key'])
    c_peer.pool.append(new_transaction)
    return jsonify(http_res.success_res)


@app.route('/get_pool', methods=['GET'])
def get_pool():
    """
    获取"数据池"里的数据
    :return:
    """
    return jsonify({
        'code': 200,
        'data': c_peer.pool
    })

@app.route('/peer_block_query', methods=['GET'])
def peer_block_query():
    """
    获取所有节点及其记录区块的索引值
    :return:
    """
    return c_peer.blockchain.peer_block

@app.route('/block_query', methods=['GET'])
def block_query():
    """
    查询指定区块索引值（高度）接口
    :return:
    """
    index = request.args['id']
    return c_peer.blockchain.query_block_info(int(index))

if __name__ == '__main__':
    print(f"{'*'*20}Starting peer1!{'*'*20}")
    scheduler.start()
    peer_socketio.run(app, host='0.0.0.0', port=http_port, debug=False)