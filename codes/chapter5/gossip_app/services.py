# -*- coding: utf-8 -*-
# File : p2p_services.py
# Author: taoyahui
# Date : 2022/3/31
import networkx as nx
import models
from datetime import datetime
import random
from flask import jsonify
import http_res

def generate_network(network_name, peer_list):
    """
    生成区块链网络，初始化Network实体，以及在Network实体中加入节点(node)和边(node)
    :param network_name: 网络名称
    :param peer_list: 已生成的节点列表
    :return: 生成的区块链网络实体对象
    """
    g_network = models.Network(network_name)
    for index, peer in enumerate(peer_list):
        g_network.add_peer(peer)
        if index == len(peer_list)-1:
            # 如果是最后一个节点，那就让最后一个节点和第一个节点收尾相连
            g_network.add_edge(peer.name, peer_list[0].name)
        else:
            # 否则，建立本节点与下一个节点的边
            g_network.add_edge(peer.name, peer_list[index+1].name)
    return g_network


def new_msg_service(body, c_peer):
    """
    HTTP接口处理函数，添加新消息处理函数
    :param body: HTTP POST 请求体内容
    :param c_peer: 当前节点对象
    :return:
    """
    if 'data' not in body:
        return jsonify(http_res.empty_res)
        # 创建新的消息(message)对象
    msg = models.Message(body['data'], datetime.now())
    # 将消息对象存储于当前节点中
    c_peer.add_message(msg.to_dict())
    c_peer.version = msg.version
    return jsonify(http_res.success_res)

def send_version(peer, network):
    """
    Socket客户端处理函数，随机发送最新数据版本服务
    :param peer: 当前节点
    :param network: 当前区块链网络
    :return:
    """
    print('start to send version!')
    peer_name = peer.name
    neighbours = list(network.G.adj[peer_name])
    rand_index = random.randint(0, len(neighbours)-1)
    neighbour_peer_name = neighbours[rand_index]
    neighbour_peer = network.G.nodes()[neighbour_peer_name]
    req_url = f"http://{neighbour_peer['host']}:{neighbour_peer['port']}"
    res_url = f"http://{peer.host}:{peer.port}"
    print(f'connect to peer {req_url}')
    peer.sio.connect(req_url)
    send_msg = {
        'version': peer.version,
        'url': res_url
    }
    peer.sio.emit('peer-version', send_msg)
    peer.sio.disconnect()


def peer_version_services(rec_msg, c_peer, sio):
    """
    用于接收socket客户端请求, message中包含节点版本(version)
    :param rec_msg: key-value形式. 包括version->请求peer的最新数据版本, url ->请求peer的url
    :param c_peer: 当前服务端节点
    :param sio: 当前服务端节点的客户端
    :return:
    """
    version = rec_msg['version']
    url = rec_msg['url']
    print(f"receive message : {version}")
    # 如果请求的消息版本号小于本节点最新节点版本号，则需取出两版本号之间的所有数据
    res_arr = []
    send_msg = {}
    if version < c_peer.version:
        # 倒序遍历，从列表最后一个元素依次遍历至索引为0的内容
        for i in range(len(c_peer.pool) - 1, -1, -1):
            get_msg = c_peer.pool[i]
            if version < get_msg['version']:
                res_arr.insert(0, get_msg)

        # 按固定格式返回数据
        send_msg = {
            'code': 1,  # 1表示存在数据
            'data': res_arr
        }
    else:
        # 当查询不到数据，则返回空数据
        send_msg = {
            'code': 0,  # 0表示不存在新数据
            'data': 'empty'
        }

    sio.connect(url)
    sio.emit('peer-message', send_msg)
    sio.disconnect()


def peer_message_service(msg_dict, c_peer):
    """
    Socket服务端接收数据服务，如果code为0表示没有新消息，code为1表示有新消息
    :param msg_json: 接收消息
    :param c_peer: 当前服务端节点
    :return:
    """
    # msg_dict = json.loads(msg)
    if 'code' not in msg_dict or 'data' not in msg_dict:
        return
    # code : 0 表示没有新数据不做任何操作
    # code : 1 表示有新数据加入"数据池"中
    if msg_dict['code'] == 0:
        return
    if msg_dict['code'] == 1:
        for get_msg in msg_dict['data']:
            msg = models.Message(get_msg['data'],
                                 datetime.strptime(get_msg['c_time'], "%Y-%m-%d %H:%M:%S"))
            c_peer.pool.append(msg.to_dict())

        c_peer.version = msg_dict['data'][-1]['version']



