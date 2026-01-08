# -*- coding: utf-8 -*-
# File : account.py
# Author: taoyahui
# Date : 2022/3/11

# 1. 什么是地址
# 由于区块链网络具有去中心化的特点，账户使用用户自定义的账户名很容易出现名称重复而无法被主动识别的问题，区块链系统中的账户通过不同的"地址"进行标识
# 地址一般是通过固定长度生成的随机字符串，长度可以为2的指数次方例如32位或64位，生成内容一般有："",""。
# 由于地址在区块链中是公开的，任何人都可以查看，为了保护对应账户的隐秘性，地址的生成方式将采用多种加密技术从而实现公开性和保密性这两个从字面里面
# 较为矛盾的条件
# 2. 地址生成的方式
# 地址在生成过程中将借助公私钥加密技术。公私钥加密技术从字面里面即为有公钥和私钥。公私钥加密技术的使用过程如下：
# 1. 生成私钥（私密密钥）的种子即"绝对"的随机数"种子"。
# 2. 通过"种子"利用某种特定的算法如：椭圆曲线加密算法、RSA加密算法等生成对应的私钥
# 3. 以私钥为基础生成对应的公钥。一般地，此过程也将借助某类特殊的加密算法
# 4. 基于公钥借助哈希等加密算法，生成地址
# 基本步骤: 生成种子 -> 生成私钥 ->  生成公钥 -> 生成地址
# 采用"绝对"随机数的原因为目前在很多随机数生成的方法中都采用了某些特定的规律，这在区块链网络信息公开的条件下很容易被不良节点利用从而破解造成损失。
# 所以"绝对"随机数的作用在于保护信息隐私的安全。接下来，将基于Python代码模拟比特币区块链系统的加密与地址生成方式进行演示，
# 借助的加密算法为椭圆曲线加密算法。
# 2.1 密钥生成
import os
import binascii
private_key =os.urandom(32)
print(private_key)
print(binascii.hexlify(private_key))

#2.2 公钥生成
# 需要预装第三方库ecdsa,操作： pip install ecdsa
import ecdsa
import binascii
public_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).verifying_key.to_string()

print(binascii.hexlify(private_key))
print(binascii.hexlify(public_key))

# 原理解释（此处略，需要详细介绍）

#2.3 地址生成
# 地址生成的具体过程如下：
# 1. 利用SHA-256将公开密钥进行哈希处理生成哈希值
# 2. 将第一步中的哈希值通过RIPEMD-160进行哈希处理后生成新的哈希值
# 3. 将第二步中的哈希值进行Base58Check编码
# 在执行如上操作时需要借助Base58第三方库，其中Base58库是一种编码方法，此类编码方法可以消除容易被人误读的字符串。其中包括的字符内容如下：
# 1. 数字0
# 2. 英文字符O
# 3. 所有英文字母的小写
# 4. 英文字母的大写
# 5. +（加号）
# 6. /(反斜杠)
# 如下为地址生成的代码

import ecdsa
import hashlib
import base58

prefix_and_pubkey = b'\x04' + public_key
intermediate = hashlib.sha256(prefix_and_pubkey).digest()
ripemd160 = hashlib.new('ripemd160')
ripemd160.update(intermediate)
hash160 = ripemd160.digest()
prefix_and_hash160 = b"\x00" + hash160

double_hash = hashlib.sha256(hashlib.sha256(prefix_and_hash160).digest()).digest()
checksum = double_hash[:4]
pre_address = prefix_and_hash160 + checksum
address = base58.b58encode(pre_address)
print("地址是:")
# 如下为生成的地址
print(address.decode())



