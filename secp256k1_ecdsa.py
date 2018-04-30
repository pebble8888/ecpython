#!/usr/bin/env python3
#
# secp256k1
# http://www.secg.org/SEC2-Ver-1.0.pdf
#  
import sys
import hashlib

sys.setrecursionlimit(1500)

b = 256
# q is prime
q = 2**256 - 2**32 - 977
# l (order of group) is prime
l = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# no depend q,l
def expmod(v,e,m):
    if e == 0: return 1
    t = expmod(v,e//2,m)**2 % m
    if e & 1: t = (t*v) % m
    return t

# no depend q,l
def inv(x, m):
    return expmod(x,m-2,m)

def double_pt(P):
    x = P[0]
    y = P[1]
    if y == 0: return [0, 0]
    nu = 3*expmod(x,2,q)*inv(2*y,q)
    x3 = expmod(nu,2,q)-2*x
    y3 = nu*(x-x3)-y
    return [x3 % q, y3 % q]

def add_pt(P, Q):
    x1 = P[0]
    y1 = P[1]
    x2 = Q[0]
    y2 = Q[1]
    if x1 == -1 and y1 == -1: return Q
    if x2 == -1 and y2 == -1: return P
    if x1 == x2:
        if (y1 + y2) % q == 0:
            return [-1, -1]
        else:
            return double_pt(P)

    lm = (y1-y2)*inv(x1-x2, q)
    x3 = expmod(lm,2,q)-(x1+x2)
    y3 = lm*(x1-x3)-y1
    return [x3 % q, y3 % q]

def scalarmult(P, e):
    if e == 0: return [-1, -1]
    Q = scalarmult(P, e//2)
    Q = add_pt(Q, Q)
    if e & 1: Q = add_pt(Q, P)
    return Q

def isoncurve(P):
    x = P[0]
    y = P[1]
    return (y**2 - x**3 - 7) % q == 0

Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = [Gx, Gy]

# big endian
def bit(h, i):
    return (h[i//8] >> (7-(i%8))) & 1

# 32 byte array to big endian integer
def decodeint(s):
    assert(len(s) == 32)
    return sum(2**(b-1-i) * bit(s,i) for i in range(0,b))

print("q  = %x" % q)
print("Gx = %x" % Gx)
print("Gy = %x" % Gy)
print("l  = %x,%d" % (l, l))
if isoncurve(G):
    print("G is on curve")
else:
    assert False, "G is not on curve!"

T = scalarmult(G, l)
print("T  = (%x, %x)" % (T[0], T[1]) )

sk = 3
PK = scalarmult(G, sk)
print("sk = %x" % sk)
print("pk = (%x, %x)" % (PK[0], PK[1]))

# string to byte array
msg = str("0000").encode('utf-8')

# -- sign

# STEP1
nonce = 2
print("nonce = %d" % nonce)
R = scalarmult(G, nonce) 
r = R[0] % l
# STEP2  check r is not 0
#   not implement
# STEP3

msg_digest = hashlib.sha256(msg).digest()
print("msg_digest:" + msg_digest.hex())
msg_i = decodeint(msg_digest)
print("msg_i:" + str(msg_i))
s = (inv(nonce,l) * (msg_i + r * sk)) % l
# STEP4  check s is not 0
#   not implement

print("r = %d" % r)
print("r = 0x%x" % r)
print("s = %d" % s)
print("s = 0x%x" % s)

# -- verify
si = inv(s,l)
u1 = (msg_i * si) % l
u2 = (r * si) % l
V = add_pt(scalarmult(G, u1), scalarmult(PK, u2)) 
print("V = (%d, %d)" % (V[0], V[1]))
result = (((V[0] - r) % l) == 0)

print("result %d" % result)
