# -*- coding: utf-8 -*-
# File : crypto_util.py
# Author: taoyahui
# Date : 2022/3/11
#使用ecdsa实现基于ecc的签名与验签
# sk为私钥，使用sk.sign可以实现签名
# 将sk生成公钥sk.verifying_key之后，使用public_key.verify方法可以实现对签名内容的验证
import ecdsa

def sign(data, private_key):
    """
    签名
    :param data: 签名时使用的数据
    :param private_key: 签名时使用的私钥
    :return:
    """
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    sig = sk.sign(data)
    return sig


def verify(data, sig, public_key):
    """
    验签
    :param data: 验签时使用的数据
    :param sig: 验签时使用的签名
    :param public_key: 验签时使用的公钥
    :return:
    """
    vk = ecdsa.VerifyingKey.from_pem(public_key)
    try:
        if vk.verify(sig, data):
            return 0    #如果验签成功则返回0
        else:
            return 1    #如果验签失败则返回1
    except Exception as e:
        return 2    #如果验签出现问题则返回2

import random

string = 'hello word'
private_key = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()', 32)).encode()
print(f'私钥是: {private_key}')
public_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).verifying_key.to_pem()
print(f'公钥是: {public_key}')
sig = sign(string.encode(), private_key)
print(f'签名是: {sig}')
print(verify(string.encode(), sig, public_key))

# print(public_key.to_string())
# str = b'hello'
# sig = sk.sign(str)
# assert public_key.verify(sig, b'hhhhh')

