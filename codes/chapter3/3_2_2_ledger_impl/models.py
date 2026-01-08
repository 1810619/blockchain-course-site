# -*- coding: utf-8 -*-
import json
import hashlib
from datetime import datetime

INITIAL_BITS = 0x1e777777     #模拟真实区块的数据设置（预留）


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
 
        :param nonce: 计算新区块的默克尔根
        （1）随机数，也称为nonce值，用于挖矿过程中的计算，如果符合难度目标，则表示这个区块被创建成功
        （2）nonce并非计算block难度的nonce，此nonce仅仅表示发送账号发送交易的次数，从0开始，每发送一次交易+1
        :param elapsed_time:运行时间
        :papam block_hash:计算区块哈希值
        """     
        self.index = index
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.elapsed_time = ""
        self.block_hash = self.calc_block_hash()

    def to_json(self):
        """
        将区块内容以JSON的形式输出
        :return: 索引号、前一区块(父块)哈希值、数据记录、时间戳、比特值、随机数、区块哈希值
        转换为十六进制，去掉0x前缀；rjust对字符串进行右对齐，宽度8，剩余位置填充0
        """
        return {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "data": self.data,
            "timestamp": self.timestamp.strftime('%Y/%m/%d %H:%M:%S'),
            'bits': hex(self.bits)[2:].rjust(8,"0"),
            'nonce': hex(self.nonce)[2:].rjust(8,"0"),
            'block_hash': self.block_hash
        }

    def calc_block_hash(self):
        """
        生成区块对应的哈希值
           连接数值对应的字符串，转换为unicode编码，用sha256算法生成哈希值，转换为16进制
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
        # self.initial_bits = initial_bits

    def add_block(self, block):
        """
        将新的区块加入区块链chain中,该方法将不被外界调用
        :param block: 新加入的区块
        :return:
        """
        self.chain.append(block)

    def query_block_info(self, index=0):
        """
        通过索引值查询区块链chain中的区块信息
        :param index: 查询区块的索引值
        :return:
        json.dumps(): Python中json模块的一个函数，用于将Python对象编码为JSON格式的字符串
        sort_keys=True 顺序排列key值，默认不为True
        如果dict包含有汉字，一定加上ensure_ascii=False：并不是所有的字符都能够被ASCII表示。
        indent=2 字符缩进为2格
        """
        return json.dumps(self.chain[index].to_json(), sort_keys=True, ensure_ascii=False, indent=2)

    def create_genesis_block(self):
        """
        创建创世区块，创世区块内容如下：
        index -> 设置为0，代表第一个区块
        prev_hash -> 设置为64个"0"作为默认参数
        data -> 存储一段字符串
        :return:
          区块初始化方法：def __init__(self, index, prev_hash, data, timestamp, bits)
        """
        genesis_block = Block(0,
                              "0" * 64,
                              "这是第一个区块（创世区块）",
                              datetime.now(),
                              INITIAL_BITS)
        self.add_block(genesis_block)

    def add_new_block(self, data):
        """
        可供调用的方法，用于添加新的区块
        :param data:
        :return:
        """
        last_block = self.chain[-1]
        # 通过last_block获取chain中的最新区块，从而获取相应的index和prev_hash
        # 用于创建新区块时使用。参数：索引值+1，上一区块的哈希值，数据记录信息，时间戳，上一区块的比特值
        block = Block(last_block.index + 1,
                      last_block.block_hash,
                      data, datetime.now(),
                      last_block.bits)
        self.chain.append(block)
        return last_block.index + 1


"""
简单的代码验证
1. 首先创建Blockchain对象
2. 输出对象的创世区块信息
3. 间隔1秒后创建一个新的区块并输出
"""
blockchain = Blockchain()
print(blockchain.query_block_info(0))
from time import sleep
sleep(1)
blockchain.add_new_block("新增的区块")
print(blockchain.query_block_info(1))
