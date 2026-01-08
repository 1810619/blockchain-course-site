# -*- coding: utf-8 -*-
# File : merkle_tree.py
# Author: taoyahui
# Date : 2022/3/10
import hashlib

# 一个默克树的类，用于实现将输入一列交易内容生成对应的默克根
#             hash_root
#          /           \
#       hash(a,b)     hash(c,d)
#       /      \      /       \
#    tx_a      tx_b tx_c       tx_d
class MerkleTree(object):
    def __init__(self, tx_list):
        self.tx_list = tx_list

    def calc_merkle_root(self):
        """
        计算默克树的根(Merkle Root)
        :return:
        """
        calc_txs = self.tx_list
        if len(calc_txs) == 1:
            return calc_txs[0]
        # 循环计算哈希值
        while len(calc_txs) > 1:
            # 若列表中的交易个数为奇数个，则在列表最后复制最后一个交易信息进行补全
            if len(calc_txs) % 2 == 1:
                calc_txs.append(calc_txs[-1])
            sub_hash_roots = []
            # 每两个交易进行组合，生成新的哈希值
            for i in range(0, len(calc_txs), 2):
                # 生成的哈希值进行累加
                sub_hash_roots.append(hashlib.sha256("".join(calc_txs[i:i+2]).encode()).hexdigest())
            # 将累加为新的哈希列表赋值为下一次循环的内容
            calc_txs = sub_hash_roots
        return calc_txs[0]


tx_list = ['1','2','3','4']
m_t = MerkleTree(tx_list)
merckle_root = m_t.calc_merkle_root();
print(merckle_root)

