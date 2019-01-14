#!/usr/bin/env python3

import base58
import hashlib

"""
BECH32CHAR="qpzry9x8gf2tvdw0s3jn54khce6mua7l"

# @param  values: int array
# @return int
def bech32_polymod(values):
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    c = 1 
    for v in values:
        t = c >> 25
        c = (c & 0x1ffffff) << 5 ^ v
        for i in range(5):
            c ^= generator[i] if ((t >> i) & 1) else 0
    return c

# @param  hrp: string
# @return int array 
def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

# @param  hrp: int
# @return data: int array
def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

# @param  hrp: string
# @param data: int array
# @return string
def bech32_encode(hrp, data):
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + '1' + ''.join([BECH32CHAR[d] for d in combined])

# @brief General power-of-2 base conversion
# @param data: int array
# @param frombits: int
# @param tobits: int
# @param pad: bool
# @return int array 
def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

# @param hrp: string
# @param witver: int 
# @param witprog: bytes
def encode(hrp, witver, witprog):
    return bech32_encode(hrp, [witver] + convertbits(witprog, 8, 5))
"""

# @param version: bytes
# @param payload: bytes
def b58check(version, payload):
    d = version + payload 
    h1digest = hashlib.sha256(d).digest()
    h2digest = hashlib.sha256(h1digest).digest()
    e = d + h2digest[0:4]
    return base58.b58encode(e)

# @param ba: bytes 
# @return 
def hash160(ba):
    d = hashlib.sha256(ba).digest()
    m = hashlib.new('ripemd160')
    m.update(d)
    return m.digest()

hrp="bc" # mainnet
#hrp="tb" # testnet
#s = encode(hrp, witver, witprog)

witver = 0
hex_pubkey = "0377fcfd729e8e580a7bf849bed9bbc44d4062e9090df097f34fb2adcb74bfc44f"
scriptid = hash160(bytes.fromhex(hex_pubkey))
print("scriptid:"+str(scriptid.hex()))
hex_scriptid = scriptid.hex()
# "7a1fccd58db0bcb244c6db4367872bbd6f43d07d"

l = len(scriptid)

#hex_witprog ="00147a1fccd58db0bcb244c6db4367872bbd6f43d07d" # seed
OP_0 = "00"
hex_len = '{:02x}'.format(l)
hex_witprog = OP_0 + hex_len + hex_scriptid
s = bytes.fromhex(hex_witprog)

#hex_version="00" # mainnet bitcoin address
#hex_version="05" # mainnet P2SH address
#hex_version = "6f" # testnet bitcoin address
hex_version = "c4" # testnet P2SH address
dest_address = b58check(bytes.fromhex(hex_version), hash160(s))
print(dest_address)

# right answer for seed
# 2N7hiJovR44NLtZr1szSKiYrNbxo9ArP8RK
