#!/usr/bin/env python

# use library
import base58
r1 = base58.b58encode("abc")
print(r1)

# not use library
alphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58encode(s):
    # 文字列をバイト配列に変換する
    v = s.encode('ascii')
    # バイト配列をBigEndianの数値と見なす
    p = 1
    s = 0
    # 右端から可算していく
    for c in reversed(v):
        s += p * c
        p = p << 8

    #   97('a') * 256 * 256 + 98('b') * 256 + 99('c') 
    # = 6356992 + 25088 + 99
    # = 6382179 
    print(s)

    output_ba = b""
    while s:
        # s に商, idx に余りが入る
        s, idx = divmod(s, 58)
        output_ba = alphabet[idx:idx+1] + output_ba

    return output_ba

r2 = b58encode("abc")
print(r2)

