#!/usr/bin/env python3

import base58
import hashlib
import hmac

hex_seed = "f04343f0d4c7396f0655edd6853422a279aebb3314c9dd362b416298b7dacb40"
seed = bytes.fromhex(hex_seed)
print(int.from_bytes(seed, 'big'))


key = "Bitcoin seed".encode('utf8')

a = hmac.new(key, seed, hashlib.sha512).hexdigest()
print(a)

x = 54272223673690410107067306572649404671112435427396683923283695463496704574543
y = 29407153271561851650417279834589029518455454545578285177340103652846543771771
print(x.to_bytes(32, 'big').hex())



