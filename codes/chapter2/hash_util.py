# -*- coding: utf-8 -*-
# File : hash_util.py
# Author: taoyahui
# Date : 2022/3/11

#   1. 引用hashlib依赖包
import hashlib
#   2. 定义需要加密的变量
words = 'Hello World'
#   3. 使用sha256算法加密
hash_code = hashlib.sha256(words.encode()).hexdigest()
#   4. 打印加密后的结果
print(hash_code)