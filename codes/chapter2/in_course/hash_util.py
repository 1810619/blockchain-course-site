# -*- coding: utf-8 -*-
# File : hash_util.py
# Author: taoyahui
# Date : 2022/9/6

import hashlib

str = "hello worldxdfsdfds"

hash_code = hashlib.sha256(str.encode()).hexdigest()

print(hash_code)
