# -*- coding: utf-8 -*-
# File : utils.py
# Author: taoyahui
# Date : 2022/3/10

from hashlib import sha256
def calc_merkle_root(data):  #构建cale_merkle_root函数
    """
    计算默克树的根(Merkle Root)
    :return:
    """
    calc_txs = [tx['id'] for tx in data]
    if len(calc_txs) == 1:
        return calc_txs[0]
    #循环计算哈希值
    while len(calc_txs) > 1:

        #若列表中的交易个数为奇数，则在列表末尾复制最后一个交易信息进行补全
        if len(calc_txs) % 2 == 1:
            calc_txs.append(calc_txs[-1])
        sub_hash_roots = []

        #组合每两个交易，生成新的哈希值
        for i in range(0, len(calc_txs), 2):
            join_str = "".join(calc_txs[i:i + 2])
            #累加生成的哈希值
            sub_hash_roots.append(sha256(join_str.encode()).hexdigest())

        #将累加得出的新的哈希列表赋值为下一次循环的内容
        calc_txs = sub_hash_roots
    return calc_txs[0]
