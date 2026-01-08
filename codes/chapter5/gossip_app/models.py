# -*- coding: utf-8 -*-
# File : models.py
# Author: taoyahui
# Date : 2022/3/31
import networkx as nx
import matplotlib.pyplot as plt
import socketio
# 区块链网络
class Network(object):
    def __init__(self, name):
        """
        初始化区块链网络
        :param name:
        """
        self.peers = []  # 网络中存在的节点
        self.name = name  # 网络名称
        self.G = nx.Graph()  # 网络中定义的networkx网络拓扑

    def add_peer(self, peer):
        """
        在网络中新增节点
        """
        self.peers.append(peer)
        self.G.add_node(peer.name, host=peer.host, port=peer.port)

    def add_edge(self, s_peer, e_peer):
        """
        在网络中新增节点间的边
        """
        e = (s_peer, e_peer)
        self.G.add_edge(*e)

    def del_peer(self, peer_name):
        """
        删除指定名称的peer节点
        """
        for i, peer in enumerate(self.peers):
            if peer_name == peer.name:
                del self.peers[i]
        self.G.remove_node(peer_name)

    def draw_network(self):
        """
        绘制网络
        """
        pos = nx.spring_layout(self.G, iterations=100)
        nx.draw(self.G, pos, with_labels=True)
        plt.show()

# 消息对象
class Message(object):
    def __init__(self, data, c_time):
        """
        初始化消息对象
        :param data: 消息内容
        :param c_time: 创建的时间
        """
        self.data = data
        self.c_time = c_time
        # 消息的版本号，用于跟踪最新数据
        self.version = int(c_time.timestamp())

    def to_dict(self):
        """
        将消息结构转为字典
        :return: 消息的字典对象
        """
        return {
            'data': self.data,
            'c_time': self.c_time.strftime("%Y-%m-%d %H:%M:%S"),
            'version': self.version
        }

# 节点对象
class Peer(object):
    def __init__(self, name, host, port):
        """
        初始化节点，
        :param name: 节点名称
        :param host: 节点的主机ip
        :param port: 节点的端口
        """
        self.name = name
        self.host = host
        self.port = port
        self.version = 0  # 节点当前最新的数据版本号
        self.pool = []  # 节点存储数据的"数据池"
        self.sio = socketio.Client()

    def add_message(self, message):
        """
        在"数据池"中添加信息
        :param message: 传入的message对象
        """
        self.pool.append(message)
