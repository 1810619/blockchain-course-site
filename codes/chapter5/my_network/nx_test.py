# -*- coding: utf-8 -*-
# File : nx_test.py
# Author: taoyahui
# Date : 2022/3/28

from chapter5.my_network import models

my_network = models.Network("test_network")
master = models.Peer("master")
peer1 = models.Peer("peer1")
peer2 = models.Peer("peer2")
peer3 = models.Peer("peer3")
peer4 = models.Peer("peer4")
my_network.add_edge("peer1", "master")
my_network.add_edge("peer2", "master")
my_network.add_edge("peer3", "master")
my_network.add_edge("peer4", "master")

my_network.add_edge("peer1", "peer2")
my_network.add_edge("peer1", "peer3")
my_network.add_edge("peer2", "peer4")
my_network.add_edge("peer3", "peer4")

my_network.draw_network()


