# -*- coding: utf-8 -*-
# File : tx_verify.py
# Author: taoyahui
# Date : 2022/3/22

import crypto_util
import models
from datetime import datetime

#   1. 创建两个账户，一个模拟发送账户一个模拟接收账户
print(f"{'*' * 10}生成第一账户{'*' * 10}")
send_account = crypto_util.create_account()
print(f"{'*' * 10}生成第二账户{'*' * 10}")
rec_account = crypto_util.create_account()
#   2. 生成一个测试交易内容
tx = models.Transaction(send_account['address'],
                        rec_account['address'],
                        "测试交易", datetime.now(), send_account['private_key'])
#   3. 验证交易正确性
verification_res = crypto_util.data_verify(tx.id, tx.sig, send_account['public_key'])
print(f'验证交易，返回结果为: {verification_res}')