# -*- coding: utf-8 -*-
# File : models.py
# Author: taoyahui
# Date : 2022/3/10
import json
import hashlib
from datetime import datetime
import binascii

from utils import sha256d

INITIAL_BITS = 0x1e777777


class Transaction(object):
    def __init__(self, sender, recipient, amount, timestamp, sig):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp
        self.sig = sig  # 私钥签名信息
        self.id = sha256d(self.to_string())

    def to_string(self):
        return f"{self.sender}{self.recipient}{self.amount}{self.timestamp.strftime('%Y/%m/%d %H:%M:%S')}"

    def to_json(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp.strftime('%Y/%m/%d %H:%M:%S'),
            "sig": binascii.hexlify(self.sig)
        }


class Block(object):
    """
    区块
    prev_hash: 上一区块的哈希值
    data: 区块中的数据
    timestamp: 区块生成的时间
    bits: 区块难度
    """

    def __init__(self, index, prev_hash, data, timestamp, bits):
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.elapsed_time = ""
        self.merkle_root = self.calc_merkle_root()
        self.block_hash = self.calc_block_hash()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def to_json(self):
        return {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "data": self.data,
            "timestamp": self.timestamp.strftime('%Y/%m/%d %H:%M:%S'),
            'bits': hex(self.bits)[2:].rjust(8, "0"),
            'nonce': hex(self.nonce)[2:].rjust(8, "0"),
            'block_hash': self.block_hash
        }

    def calc_merkle_root(self):
        """
        计算默克树的根(Merkle Root)
        :return:
        """
        calc_txs = self.data
        if len(calc_txs) == 1:
            return calc_txs[0]
        while len(calc_txs) > 1:
            if len(calc_txs) % 2 == 1:
                calc_txs.append(calc_txs[-1])
            sub_hash_roots = []
            for i in range(0, len(calc_txs), 2):
                sub_hash_roots.append(hashlib.sha256("".join(calc_txs[i:i+2])))
            calc_txs = sub_hash_roots
        return calc_txs[0]


    def calc_block_hash(self):
        """
        生成区块对应的哈希
        :return:
        """
        blockheader = str(self.index) + str(self.prev_hash) \
                      + str(self.data) + str(self.timestamp) \
                      + hex(self.bits)[2:] + str(self.nonce) + self.merkle_root
        h = sha256d(blockheader.encode())
        return h


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
        # self.initial_bits = initial_bits

    def add_block(self, block):
        self.chain.append(block)

    def query_block_info(self, index=0):
        return json.dumps(self.chain[index].to_json(), sort_keys=True, ensure_ascii=False, indent=2)

    def create_genesis_block(self):
        genesis_block = Block(0, "0" * 64, "这是第一个区块（创世区块）", datetime.now(), INITIAL_BITS)
        self.add_block(genesis_block)

    def add_new_block(self, data):
        last_block = self.chain[-1]
        block = Block(last_block.index + 1, last_block.block_hash, data, datetime.now(), last_block.bits)
        self.chain.append(block)
        return last_block.index + 1

# 在现实
class Peer:
    def __init__(self):
        self.tx_pool = []

    def add_tx(self, tx):
        self.tx_pool.append(tx)

    def clear_pool(self):
        self.tx_pool = []
