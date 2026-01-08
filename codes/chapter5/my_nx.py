# -*- coding: utf-8 -*-
# File : my_nx.py
# Author: taoyahui
# Date : 2022/3/27

import networkx as nx
import matplotlib.pyplot as plt

a_ip = '192.168.1.1'
b_ip = '192.168.1.2'
c_ip = '192.168.1.3'
G = nx.Graph()
G.add_node(a_ip)
G.add_nodes_from([b_ip, c_ip])
G.add_edge(a_ip, b_ip)
e = (b_ip,c_ip)
G.add_edge(*e)
nx.draw_shell(G, with_labels=True)
plt.show()

