# -*- coding: utf-8 -*-
# File : block_verify.py
# Author: taoyahui
# Date : 2022/3/22
import models
import crypto_util
from datetime import datetime
import utils

#   1. 创建区块链
blockchain = models.Blockchain()

#   2.创建两个账户，一个模拟发送账户一个模拟接收账户
print(f"{'*' * 10}生成第一账户{'*' * 10}")
send_account = crypto_util.create_account()
print(f"{'*' * 10}生成第二账户{'*' * 10}")
recv_account = crypto_util.create_account()

#   3.加入10条交易记录
tx_list = []
for index in range(0, 10):
    tx_list.append(models.Transaction(send_account['address'],
                                      recv_account['address'],
                                      f"第{index}条测试交易",
                                      datetime.now(),
                                      send_account['private_key']))
#   4. 将交易打包进入区块链
index = blockchain.add_new_block(data=tx_list)
block1 = blockchain.query_block_info(1)
block_1_merkle_root = block1['merkle_root']
print(f"第一个区块的Merkle Root为: {block_1_merkle_root}")

#   5. 验证
verify_merkle_root = utils.calc_merkle_root(block1['data'])
print(f"验证的Merkle Root为: {verify_merkle_root}")
if verify_merkle_root == block_1_merkle_root:
    print("验证成功")
else:
    print("验证失败")