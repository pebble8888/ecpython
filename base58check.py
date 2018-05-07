#!/usr/bin/env python

import base58
import hashlib

# version: 1 byte
# payload: bytes
def b58check(version, payload):
    d = version + payload 
    h1digest = hashlib.sha256(d).digest()
    h2digest = hashlib.sha256(h1digest).digest()
    e = d + h2digest[0:4]
    return base58.b58encode(e)

ba = bytes.fromhex("037c3e90284927ea5a46cb7f4d8c91a5d6defd3827144b28ad2451b524becb9806")
d = hashlib.sha256(ba).digest()
m = hashlib.new('ripemd160')
m.update(d)
ba = m.digest()

r1 = b58check(bytes.fromhex("00"), ba) 
print(r1)

