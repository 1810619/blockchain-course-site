# -*- coding: utf-8 -*-
# File : models.py
# Author: taoyahui
# Date : 2022/3/21

import json
import hashlib
from datetime import datetime
from crypto_util import data_sign, sha256d
import binascii

INITIAL_BITS = 0x1e777777   # 此配置为模拟真实区块的数据设置（预留）

# 预置一个私钥，用于创建创世区块使用
d_pk = """-----BEGIN EC PRIVATE KEY-----\nMHQCAQEEIClncSpsc2Fua3ljeiR2aCNydSFkbXQoQHAleGZlYiZqoAcGBSuBBAAK\noUQDQgAEyTx/sAlhdNUOwcfnCjOVp9fxMF6DUwSLkFqj2E6sDFuPVrKF9wVWH8J3\nntxWh+kR3GFKcB48v3eTfElUs5L7Zw==\n-----END EC PRIVATE KEY-----\n"""

class Transaction(object):
    def __init__(self, sender, recipient, data, timestamp, private_key):
        """
        交易的初始化
        :param sender: 发送者的地址
        :param recipient: 接收者的地址
        :param data: 交易的内容
        :param timestamp: 交易的时间戳
        :param private_key: 发送者的私钥
        """
        self.sender = sender
        self.recipient = recipient
        self.data = data
        self.timestamp = timestamp
        # 生成交易的哈希值
        self.id = sha256d(self.to_string())
        # 生成签名
        self.sig = data_sign(self.id, private_key)

    def to_string(self):
        """
        将交易元素拼接为一个字符串
        :return:
        """
        return f"{self.sender}{self.recipient}{self.data}" \
               f"{self.timestamp.strftime('%Y/%m/%d %H:%M:%S')}"

    def to_json(self):
        """
        将交易元素转变为一个DICT对象
        :return:
        """
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "data": self.data,
            "timestamp": self.timestamp.strftime('%Y/%m/%d %H:%M:%S'),
            "sig": binascii.hexlify(self.sig).decode(),
        }


# 区块对象
class Block(object):
    def __init__(self, index, prev_hash, data, timestamp, bits):
        """
        区块的初始化方法，在创建一个区块需传入包括索引号等相关信息
        :param index: 区块索引号
        :param prev_hash: 前一区块的哈希值
        :param data: 区块中需保存的记录
        :param timestamp: 区块生成的时间戳
        :param bits: 区块需传入的比特值（预留）
        """
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        # 计算新区块的默克根
        self.merkle_root = self.calc_merkle_root()
        # 计算区块的哈希值
        self.block_hash = self.calc_block_hash()

    def to_json(self):
        """
        将区块内容以JSON的形式输出
        :return:
        """
        tx_list = [tx.to_json() for tx in self.data]
        # tx_json = json.dumps(tx_list, indent=3)
        return {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "merkle_root": self.merkle_root,
            "data": tx_list,
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
        calc_txs = [tx.id for tx in self.data]
        if len(calc_txs) == 1:
            return calc_txs[0]
        while len(calc_txs) > 1:
            if len(calc_txs) % 2 == 1:
                calc_txs.append(calc_txs[-1])
            sub_hash_roots = []
            for i in range(0, len(calc_txs), 2):
                join_str = "".join(calc_txs[i:i+2])
                sub_hash_roots.append(hashlib.sha256(join_str.encode()).hexdigest())
            calc_txs = sub_hash_roots
        return calc_txs[0]

    def calc_block_hash(self):
        """
        生成区块对应的哈希值
        :return:
        """
        blockheader = str(self.index) + str(self.prev_hash) \
                      + str(self.data) + str(self.timestamp) + \
                      hex(self.bits)[2:] + str(self.nonce)
        h = hashlib.sha256(blockheader.encode()).hexdigest()
        self.block_hash = h
        return h


# 区块链对象，包括一个以chain为对象的数组
class Blockchain(object):
    def __init__(self):
        """
        初始化区块链对象，操作包括：
        1、定义一个以chain命名的区块链数组
        2、在链中加入创世区块(genesis block)
        """
        self.chain = []
        self.create_genesis_block()

    def add_block(self, block):
        self.chain.append(block)

    def query_block_info(self, index=0):
        """
        通过索引值查询区块链chain中的区块信息
        """
        block_json = self.chain[index].to_json()
        return block_json

    def create_genesis_block(self):
        """
        创建创世区块
        """
        tx = Transaction("0" * 32, "0" * 32, "第一笔交易", datetime.now(), d_pk)
        genesis_block = Block(0,
                              "0" * 64,
                              [tx],
                              datetime.now(),
                              INITIAL_BITS)
        self.add_block(genesis_block)

    def add_new_block(self, data):
        last_block = self.chain[-1]
        block = Block(last_block.index + 1,
                      last_block.block_hash,
                      data,
                      datetime.now(),
                      last_block.bits)
        self.chain.append(block)
        return last_block.index + 1


# 模拟的节点
class Peer:
    def __init__(self):
        self.tx_pool = []

    def add_tx(self, tx):
        self.tx_pool.append(tx)

    def clear_pool(self):
        self.tx_pool = []


