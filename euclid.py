#!/usr/bin/env python3

from fractions import gcd

def gcd(a, b):
    if a < b:
        t = a
        a = b
        b = t

    last_r = b
    while True:
        c = a // b
        r = a - c * b
        #print(str(a)+" = "+str(c)+" * "+str(b)+" + "+str(r))
        if r == 0:
            #print("")
            return last_r 
        last_r = r
        a = b
        b = r

def lcm(a, b):
    return (a * b) // gcd(a, b)

#d = gcd(11921192, 41414141)
#print(d)

