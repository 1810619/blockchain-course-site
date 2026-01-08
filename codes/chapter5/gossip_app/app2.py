# -*- coding: utf-8 -*-
# File : app0.py
# Author: taoyahui
# Date : 2022/4/1

from flask import Flask, request, jsonify
import flask_socketio
import services
import entity
import models
import http_res
from datetime import datetime
from flask_apscheduler import APScheduler
import socketio
import json

network = entity.network  # 获取区块链网络内容
c_peer = entity.peer2  # 取出当前进程的节点内容
app = Flask(__name__)

# 创建socket客户端
scheduler = APScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True
app.config.from_object(Config())
scheduler.init_app(app)

"""
misfire_grace_time:单位为秒,假设有这么一种情况,当某一job被调度时刚好线程池都被占满,调度器会选择将该job排队不运行,misfire_grace_time
参数则是在线程池有可用线程时会比对该job的应调度时间跟当前时间的差值,如果差值<misfire_grace_time时,调度器会再次调度该job.反之该job的执行状态为EVENT_JOB_MISSED了,即错过运行.
"""
@scheduler.task('interval', id='send_message', seconds=20, misfire_grace_time=900)
def send_message():
    services.send_version(c_peer, network)

peer_socketio = flask_socketio.SocketIO(app, cors_allowed_origins='*')

@peer_socketio.on('peer-version')
def peer_version(rec_msg):
    services.peer_version_services(rec_msg, c_peer, c_peer.sio)

@peer_socketio.on('peer-message')
def peer_message(msg_dict):
    services.peer_message_service(msg_dict, c_peer)

@app.route('/new_msg', methods=['POST'])
def new_msg():
    """
    用于接收用户新消息请求，数据将存储于对应节点的"数据池"中
    :return:
    """
    body = request.json
    return services.new_msg_service(body, c_peer)
    # body = request.json
    # if 'data' not in body:
    #     return jsonify(http_res.empty_res)
    # # 创建新的消息(message)对象
    # msg = models.Message(body['data'], datetime.now())
    # #将消息对象存储于当前节点中
    # c_peer.add_message(msg.to_dict())
    # c_peer.version = msg.version
    # return http_res.success_res

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

if __name__ == '__main__':
    print(f"{'*'*20}Starting peer2!{'*'*20}")
    scheduler.start()
    peer_socketio.run(app, host='0.0.0.0', port=5002, debug=False)
