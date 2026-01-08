# -*- coding: utf-8 -*-
# File : models.py
# Author: taoyahui
# Date : 2022/3/13
import networkx as nx
import matplotlib.pyplot as plt


class Network(object):
    def __init__(self, name):
        self.peers = []
        self.name = name
        self.G = nx.Graph()

    def add_peer(self, peer):
        self.peers.append(peer)
        self.G.add_node(peer.name)

    def add_edge(self, s_peer, e_peer):
        e = (s_peer, e_peer)
        self.G.add_edge(*e)

    def del_peer(self, peer_name):
        """
        删除指定名称的peer节点
        :param peer_name:
        :return:
        """
        for i, peer in enumerate(self.peers):
            if peer_name == peer.name:
                del self.peers[i]
        self.G.remove_node(peer_name)

    def draw_network(self):
        pos = nx.spring_layout(self.G, iterations=100)
        nx.draw(self.G, pos, with_labels=True)
        plt.show()


class Peer(object):
    def __init__(self, name):
        self.name = name
        self.mem_pool = []
        self.blockchain = []

    def broadcast_transaction(self):
        """
        广播交易
        :return:
        """
        pass

    def broadcast_block(self):
        """
        广播区块
        :return:
        """
        pass







