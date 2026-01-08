# -*- coding: utf-8 -*-
# File : p2p_services.py
# Author: taoyahui
# Date : 2022/4/8
import models
import entity
import pow
from datetime import datetime

def generate_network(network_name, peer_list):
    """
    生成区块链网络
    """
    g_network = models.Network(network_name)
    for index, peer in enumerate(peer_list):
        g_network.add_peer(peer)
        if index == len(peer_list)-1:
            g_network.add_edge(peer.name, peer_list[0].name)
        else:
            g_network.add_edge(peer.name, peer_list[index+1].name)
    return g_network

def exe_pow(data, peer_name):
    """
    供节点循环执行PoW算法
    :param data: 区块数据
    :param peer_name: 节点名称
    """
    # 1. 首先获取区块链中最新区块
    last_block = entity.blockchain.chain[-1]
    # 2. 获取last_block区块的索引值（即区块高度）
    index = last_block.index + 1
    # 3. 生成新的区块
    g_block = models.Block(last_block.index + 1, last_block.prev_hash,
                           data, datetime.now(), last_block.difficult_bits)
    # 4. 将区块扔入pow算法中进行计算，在得到区块头后返回区块信息
    c_block = pow.pow_alg(g_block)
    # 判断区块链内的内容，如果当前区块链中没有新数据产生，则将产生的区块加入到区块链中
    if len(entity.blockchain.chain) <= index:
        entity.blockchain.add_block(c_block)
        entity.blockchain.add_peer_block(peer_name, index)
    else:
        # 如果计算的区块索引已存在，则说明其他节点已抢先计算完成，则计算失败不能将结果保存至区块链
        print(f'区块索引<{index}>，已存在！{peer_name}节点计算失败')
