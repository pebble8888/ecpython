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
    if e < 0: e = e + l
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

# 32 byte array to big endian integer
def decodeint(s):
    assert(len(s) == 32)
    return int.from_bytes(s, 'big')

# big endian integer to 32 byte array
def encodeint(y):
  return y.to_bytes(32, byteorder='big')

print("q  = {}".format(q))
print("l  = {}".format(l))

# string to byte array
msg = str("0000").encode('utf-8')

# -- schnorr sign 
x = 5
print("x = {}".format(x))
Y = scalarmult(G, -x)
print("Y  = ({0}, {1})".format(Y[0], Y[1]))
r = 2
print("r  = {}".format(r))
U = scalarmult(G, r) 
u = U[0]

# int to byte array
u_ba = encodeint(u)
e_digest = hashlib.sha256(u_ba + msg).digest()
e = decodeint(e_digest)
v = (r + x * e) % l

print("e  = {}".format(e))
print("v  = {}".format(v))

# -- verify
UD = add_pt(scalarmult(G, v), scalarmult(Y, e))
ud = UD[0] % l
ud_ba = encodeint(ud)

ed_digest = hashlib.sha256(ud_ba + msg).digest()
ed = decodeint(ed_digest)
print("ed = {}".format(ed))

print("result {}".format(e == ed))

