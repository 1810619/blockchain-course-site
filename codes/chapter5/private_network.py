# -*- coding: utf-8 -*-
# File : private_network.py
# Author: taoyahui
# Date : 2022/3/29
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_node(0)
for i in range(1,30):
    G.add_node(i)
    G.add_edge(0,i)

# 对绘制的图形进行配置，配置其中节点大小为50
options = {
    'node_size': 50,
}
nx.draw(G,**options)
plt.show()
