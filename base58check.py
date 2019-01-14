#!/usr/bin/env python3

import base58
import hashlib

# version: bytes
# payload: bytes
def b58check(version, payload):
    d = version + payload 
    h1digest = hashlib.sha256(d).digest()
    h2digest = hashlib.sha256(h1digest).digest()
    e = d + h2digest[0:4]
    return base58.b58encode(e)

def hash160(ba):
    d = hashlib.sha256(ba).digest()
    m = hashlib.new('ripemd160')
    m.update(d)
    return m.digest()

#pubkeyhex = "0307be6887e97bf74882ff3bb73aab63f7fe48931bbc7281c5d325606f683cbaf0"
#pubkeyhex = "0377fcfd729e8e580a7bf849bed9bbc44d4062e9090df097f34fb2adcb74bfc44f"
#pubkeyhex = "03468067c38b846a4af20520b0aae8dcd344391770d200eaf82cc8f391a44c6845"
#ba = bytes.fromhex(pubkeyhex)
#ba = hash160(ba)

ba = bytes.fromhex("00147a1fccd58db0bcb244c6db4367872bbd6f43d07d")

# 00: mainnet bitcoin address
# 6f: testnet bitcoin address
# 05: mainnet P2SH address
# c4: testnet P2SH address
#hex_version = "00"
#hex_version = "6f"
a = "c4"
r1 = b58check(bytes.fromhex(hex_version), ba) 
print(r1)

