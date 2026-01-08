# -*- coding: utf-8 -*-
import random
import ecdsa
#   1. 生成种子
#   random.sample():从指定序列中随机获取指定长度的片断并随机排列，结果以列表的形式返回
#   str.join(item): 用str将item的每个成员连接起来
#   str.encode(): 将字符串编码为字节序列。默认情况使用UTF-8编码，但也可以指定其他编码方式
seed = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*()', 32)).encode()
#   2. 生成私钥。通过 ecdsa.SigningKey.from_string方法重建出符合要求的签名钥匙/私钥
#   .to_pem():以可读的文本形式表示私钥
private_key = ecdsa.SigningKey.from_string(seed, curve=ecdsa.SECP256k1).to_pem()
#   3. 生成公钥
public_key = ecdsa.SigningKey.from_pem(private_key).verifying_key.to_pem()
print(f' {private_key}')
print(f' {public_key}')
