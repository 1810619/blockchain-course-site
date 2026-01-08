# -*- coding: utf-8 -*-
# File : p2p_services.py
# Author: taoyahui
# Date : 2022/4/8
import models
import entity
import random
from datetime import datetime
import time


#定义目标值的生成函数
def generate_target(difficult_bits):
    """
    基于区块难度生成对应的目标值
    :param difficult_bits: 区块难度
    :return:
    """
    # 取区块难度(16进制数)的前2位作为指数
    exponent = int(difficult_bits / 16 ** 6)
    # 取区块难度(16进制数)的后6位作为系数
    coefficient = int(difficult_bits % 16 ** 6)
    print(f'exponent is {hex(exponent)}')
    print(f'coefficient is {hex(coefficient)}')
    # 按照共识计算目标值
    target = coefficient * 2 ** (8 * (exponent - 0x03))
    print(f'target is {target}')
    # 将目标值转变为16进制表示的值
    target_hex = hex(target)[2:].zfill(64)
    print(f'target_hex is {target_hex}')
    return target

#定义pow算法
def pow_alg(block):
    #获取指定区块的难度
    difficult_bits = block.difficult_bits
    #生成目标值
    target = generate_target(difficult_bits)

    # 通过循环的方式反复生成区块头的哈希值并与目标值比较
    # 设置计算次数为2的32次方，若循环超出计算次数则停止运算
    # 每次循环将区块中的"随机值"累加1，并生成新的哈希值与目标值比较
    for n in range(2 ** 32):
        block.nonce = block.nonce + n
        block.calc_block_hash()
        # print(f'block_hash hex is {hex(int(block.block_hash, 16))}')
        # 当block_hash小于目标值target则说明符合条件
        if int(block.block_hash, 16) < target:
            print(f'{"*" * 20}完成计算！{"*" * 20}')
            print(f'总共计算了: {block.nonce} 次')
            print(f'target hex值为: {hex(target)[2:].zfill(64)}')
            print(f'区块哈希值为: {hex(int(block.block_hash, 16))[2:].zfill(64)}')
            return block


def exe_pow(data, peer):
    """
    供节点循环执行PoW算法
    :param data: 当前节点中保存的交易池(pool)数据
    :param peer_name: 节点名称
    """
    print(f" {'*' * 20}{peer.name} start to execute pow!{'*' * 20}")
    # 1. 首先获取区块链中最新区块
    last_block = peer.blockchain.chain[-1]
    # 2. 获取last_block区块的索引值（即区块高度）
    index = last_block.index + 1
    # 3. 生成新的区块

    g_block = models.Block(last_block.index + 1, last_block.prev_hash,
                           data, datetime.now(), last_block.difficult_bits)
    g_block.gen_merkle_root_and_block_hash()
    # 4. 将区块扔入pow算法中进行计算，在得到区块头后返回区块信息
    c_block = pow_alg(g_block)
    # 判断区块链内的内容，如果当前区块链中没有新数据产生，则将产生的区块加入到区块链中
    if len(peer.blockchain.chain) <= index:
        peer.blockchain.add_block(c_block)
        peer.blockchain.add_peer_block(peer.name, index)
        peer.last_block = index
    else:
        # 如果计算的区块索引已存在，则说明其他节点已抢先计算完成，则计算失败不能将结果保存至区块链
        print(f'区块索引<{index}>，已存在！{peer.name}节点计算失败')
