# -*- coding: utf-8 -*-
# File : utils.py
# Author: taoyahui
# Date : 2022/3/10
from hashlib import sha256

def calc_merkle_root(data):
    """
    计算默克树的根(Merkle Root)
    :return:
    """
    calc_txs = [tx.id for tx in data]
    if len(calc_txs) == 1:
        return calc_txs[0]
    while len(calc_txs) > 1:
        if len(calc_txs) % 2 == 1:
            calc_txs.append(calc_txs[-1])
        sub_hash_roots = []
        for i in range(0, len(calc_txs), 2):
            join_str = "".join(calc_txs[i:i + 2])
            sub_hash_roots.append(sha256(join_str.encode()).hexdigest())
        calc_txs = sub_hash_roots
    return calc_txs[0]