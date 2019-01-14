#!/usr/bin/env python3

# string to bytearray
a = "012".encode("utf8")
print(a)

# bytearray to hex
b = b'\xde\xad\xbe\xef'.hex()
print(b)

# bytes to int
int.from_bytes(b'\xde\xad\xbe\xef', 'big')

# int to bytes
128.to_bytes(2, 'big') # 2バイトでbig


