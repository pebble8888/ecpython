#!/usr/bin/env python 

from ec import EC 
from ec import Point

ec = EC(0, 0, 7, 31)
print("order:" + str(ec.order))
G = Point(1, 15)
print("G:" + G.desc())
R = Point(25, 15)
print("R:" + R.desc())

def exhaustive_search(G, R, ec):
    x = 1
    while x < ec.order:
        S = ec.mul(G, x)
        if S.is_equal(R):
            return x
        x += 1

x = exhaustive_search(G, R, ec)
print("x:" + str(x))

