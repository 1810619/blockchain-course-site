# -*- coding: utf-8 -*-
# File : multi_center_network.py
# Author: taoyahui
# Date : 2022/3/28
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
# 创建中心节点，绘制中心节点间的边，实现相互联结
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_edge(0,1)
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(5,0)

# 为每个中心节点创建子节点
for i in range(0,6):
    for j in range(0,5):
        sub_node = f'{i}{j}'
        G.add_node(sub_node)
        G.add_edge(i,sub_node)
options = {
    'node_size': 50,
}
nx.draw(G,**options)
plt.show()

