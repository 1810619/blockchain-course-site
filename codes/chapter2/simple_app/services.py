# -*- coding: utf-8 -*-
# File : p2p_services.py
# Author: taoyahui
# Date : 2022/4/25
import hashlib

def hash_encrypt(input):
    """
    使用哈希算法加密
    :param input: 客户端发送的数据
    :return: 返回给客户端的加密数据
    """
    hash_code = hashlib.sha256(input.encode()).hexdigest()
    return hash_code

