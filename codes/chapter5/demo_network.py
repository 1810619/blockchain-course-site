# -*- coding: utf-8 -*-
# File : demo_network.py
# Author: taoyahui
# Date : 2022/3/29
import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)

G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
nx.draw(G)
plt.show()
