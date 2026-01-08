# -*- coding: utf-8 -*-
# File : decentral_network.py
# Author: taoyahui
# Date : 2022/3/28

import networkx as nx
import matplotlib.pyplot as plt
# gnp_random_graph可随机生成图形网络，传入参数的含义分别为：
# 1. 节点数量，示例参数50表示网络中包含50个节点
# 2. 网络节点连接的复杂度，示例参数0.08表示节点间边的连接复杂度
G = nx.gnp_random_graph(50,0.08)
options = {
    'node_size':50,
}
nx.draw(G, **options)
plt.show()
# plt.savefig('network.png')


