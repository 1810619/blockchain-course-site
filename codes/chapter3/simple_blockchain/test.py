# -*- coding: utf-8 -*-
# File : nx_test.py
# Author: taoyahui
# Date : 2022/3/9

import models

blockchain = models.Blockchain()
print(blockchain.query_block_info(0))
from time import sleep
sleep(1)
blockchain.add_new_block("新增的区块")
print(blockchain.query_block_info(1))
