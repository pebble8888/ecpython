#!/usr/bin/env python

# use library
import base58
r1 = base58.b58encode(b'\x00\x01\x02')
print(r1)

# not use library
alphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58encode(v):
    nPad = len(v)
    v = v.lstrip(b'\0')
    nPad -= len(v)
    # バイト配列をBigEndianの数値と見なす
    p = 1
    s = 0
    # 右端から可算していく
    for c in reversed(v):
        s += p * c
        p = p << 8

    #   0 * 256 * 256 + 1 * 256 + 2
    # = 258
    print(s)

    output_ba = b''
    while s:
        # s に商, idx に余りが入る
        s, idx = divmod(s, 58)
        output_ba = alphabet[idx:idx+1] + output_ba

    # 先頭の0x0 の nPad バイト分ある場合は0(base58では1)を nPad バイト分パディングする
    return alphabet[0:1] * nPad + output_ba

r2 = b58encode(b'\x00\x01\x02')
print(r2)

