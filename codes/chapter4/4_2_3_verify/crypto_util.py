# -*- coding: utf-8 -*-
# File : crypto_util.py
# Author: taoyahui
# Date : 2022/3/22
import binascii

import ecdsa
import random
import hashlib
import base58
from hashlib import sha256


def create_seed():
    """
    创建密钥对应的种子
    :return:
    """
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()', 32)).encode()


def create_private_key(seed):
    """
    使用种子创建密钥
    :param seed:私钥生成需要的种子
    :return:
    """
    return ecdsa.SigningKey.from_string(seed, curve=ecdsa.SECP256k1).to_pem()


def create_public_key(private_key):
    """
    使用私钥生成公钥
    :param private_key:
    :return:
    """
    return ecdsa.SigningKey.from_pem(private_key).verifying_key.to_pem()

def sha256d(string):
    """
    将字符串转为哈希值
    :param string:
    :return:
    """
    if not isinstance(string, bytes):
        string = string.encode()

    return sha256(sha256(string).digest()).hexdigest()

# 地址生成的具体过程如下：
# 1. 利用SHA-256将公开密钥进行哈希处理生成哈希值
# 2. 将第一步中的哈希值通过RIPEMD-160进行哈希处理后生成新的哈希值
# 3. 将第二步中的哈希值记性Base58编码
def create_account():
    """
    生成账户
    :return:
    """
    new_seed = create_seed()
    private_key_pem = create_private_key(new_seed)
    public_key_pem = create_public_key(private_key_pem)
    in_public_key = ecdsa.VerifyingKey.from_pem(public_key_pem).to_string()
    intermediate = hashlib.sha256(in_public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(intermediate)
    hash160 = ripemd160.digest()

    double_hash = hashlib.sha256(hashlib.sha256(hash160).digest()).digest()
    checksum = double_hash[:4]
    pre_address = hash160 + checksum
    address = base58.b58encode(pre_address)
    print(f"生成地址是: {address.decode()}")
    return {
        "address": address.decode(),
        'private_key': private_key_pem.decode(),
        'public_key': public_key_pem.decode()
    }


def data_sign(data, private_key):
    """
    签名
    :param data: 签名时使用的数据
    :param private_key: 签名时使用的私钥
    :return: 签名的内容
    """
    if not isinstance(data, bytes):
        data = data.encode()
    sk = ecdsa.SigningKey.from_pem(private_key)
    sig = sk.sign(data)
    return sig


def data_verify(data, sig, public_key):
    """
    验签
    :param data: 验签时使用的数据
    :param sig: 验签时使用的签名
    :param public_key: 验签时使用的公钥
    :return: 验签的结果
    """
    if not isinstance(data, bytes):
        data = data.encode()
    vk = ecdsa.VerifyingKey.from_pem(public_key)
    try:
        if vk.verify(sig, data):
            return 0    #如果验签成功则返回0
        else:
            return 1    #如果验签失败则返回1
    except Exception as e:
        print(e)
        return 2    #如果验签出现问题则返回2
