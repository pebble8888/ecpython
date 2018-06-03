#!/usr/bin/env python

import hashlib
h = hashlib.new('ripemd160')
h.update(b"abc")
r1 = h.hexdigest()

print(r1)
print("len "+str(len(r1)))
