# -*- coding: utf-8 -*-
# File : crypto_util.py
# Author: taoyahui
# Date : 2022/3/22
#import binascii

import ecdsa    #python第三方库，需要安装：pip install ecdsa
import random   #python标准库，生成随机数
import hashlib  #python标准库，提供了用于加密哈希算法的功能。hashlib模块支持多种哈希算法，如MD5、SHA1、SHA256等
import base58   #需要安装：pip install base58
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

'''
def sha256d(string):
    """
    将字符串转为哈希值
    :param string:
    :return:
    """
    if not isinstance(string, bytes):
        string = string.encode()

    return sha256(sha256(string).digest()).hexdigest()
'''

# 地址生成的具体过程如下：
# 1. 利用SHA-256将公开密钥进行哈希处理生成哈希值（intermediate）
# 2. 将第一步中的哈希值通过RIPEMD-160、两次SHA-256进行哈希处理后生成新的哈希值（double_hash）
# 3. 将第二步中的哈希值记性Base58编码
def create_account():
    """
    生成账户
    :return:账户三要素：地址、私钥、公钥
    """
    new_seed = create_seed()
    private_key_pem = create_private_key(new_seed)
    public_key_pem = create_public_key(private_key_pem)
    in_public_key = ecdsa.VerifyingKey.from_pem(public_key_pem).to_string()
    #中间哈希值。.digest()用于返回摘要信息，返回值为二进制字符串，长度与选择的算法有关。SHA-256，32字节长
    intermediate = hashlib.sha256(in_public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(intermediate)
    hash160 = ripemd160.digest()

    #第二个哈希值。两次哈希计算
    double_hash = hashlib.sha256(hashlib.sha256(hash160).digest()).digest()
    checksum = double_hash[:4]   #切片，取字符串前四位
    pre_address = hash160 + checksum
    #base58编码。解码方式：base58.b58decode()
    address = base58.b58encode(pre_address) 
    print(f"生成地址是: {address.decode()}")
    return {
        "address": address.decode(),
        'private_key': private_key_pem.decode(),
        'public_key': public_key_pem.decode()
    }

print(create_account())


'''
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

'''
