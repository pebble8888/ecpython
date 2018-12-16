#!/usr/bin/env python3

from fractions import gcd
import operator

class Pol:
    def __init__(self, units):
        self.units = units
        self.normalize()

    def normalize(self):
        l_units = []
        for u in self.units:
            found = False
            for l_u in l_units:
                if u.power == l_u.power:
                    l_u.coef += u.coef
                    found = True
                    break
            if not found:
                l_units.append(u)
        self.units = [x for x in l_units if x.coef != 0]
        self.units.sort(key=operator.attrgetter('power'), reverse=True)

    def highestUnit(self):
        unit = Unit(0, 0) 
        for u in self.units:
            if unit.power < u.power:
                unit = u
        return unit

    def __add__(self, other):
        l_units = self.units
        l_units.extend(other.units)  
        return Pol(l_units)
    
    def __sub__(self, other):
        l_units = self.units
        for i in other.units:
            l_units.append(-i)
        return Pol(l_units)

    def __mul__(self, other):
        l_units = []
        for i in self.units:
            for j in other.units:
                l_units.append(i * j)
        return Pol(l_units)

    def __mod__(self, other):
        o_h = other.highestUnit()
        assert(o_h.coef == 1)
        tmp = self
        while True:
            tmp_h = tmp.highestUnit()
            if tmp_h.power < o_h.power:
                break
            p = Pol([Unit(tmp_h.coef, tmp_h.power - o_h.power)])
            tmp = tmp - p * other  
        return tmp

    def iszero(self):
        return len(self.units) == 0

    def is_gcd_one(self, other):
        return (self % other).iszero()

    def __str__(self):
        if self.iszero():
            return "0"
        s = ""
        for u in self.units:
            s += " + " + str(u)  
        return s.strip(" + ")

class Unit:
    def __init__(self, coef, power): 
        self.coef = coef
        self.power = power

    def __str__(self):
        if self.power == 0:
            return str(self.coef)     
        s = ""
        if self.coef != 1:
            s += str(self.coef) 
        if self.power == 1:
            s += "x"
        else:
            s += "x^"+str(self.power)
        return s

    def __add__(self, other):
        assert(self.power == other.power)
        return Unit(self.coef + other.coef, self.power)

    def __sub__(self, other):
        assert(self.power == other.power)
        return Unit(self.coef - other.coef, self.power)

    def __neg__(self):
        return Unit(- self.coef, self.power) 

    def __mul__(self, other):
        return Unit(self.coef * other.coef, self.power + other.power)

    def __floordiv__(self, other):
        return Unit(self.coef // other.coef, self.power - other.power)

    def iszero(self):
        return self.coef == 0

#def gcd(a, b):
#    if a < b:
#        t = a
#        a = b
#        b = t
#
#    last_r = b
#    while True:
#        c = a // b
#        r = a - c * b
#        #print(str(a)+" = "+str(c)+" * "+str(b)+" + "+str(r))
#        if r == 0:
#            #print("")
#            return last_r 
#        last_r = r
#        a = b
#        b = r

def lcm(a, b):
    return (a * b) // gcd(a, b)

#d = gcd(11921192, 41414141)
#print(d)

#d = lcm(2, 3)
#print(d)

#u = Unit(3, 2)
#print(u)

p = Pol([Unit(-1, 0), Unit(1, 5)])
print("P = " + str(p))

q = Pol([Unit(1, 3), Unit(2, 1), Unit(1, 0)])
print("Q = " + str(q))

r = p * q
print("P * Q = " + str(r))

s = p % q
print("P mod Q = " + str(s))

u = Pol([Unit(1, 8), Unit(2, 6), Unit(1, 5), Unit(-1, 3), Unit(-2, 1), Unit(-1, 0)])
print("U = " + str(u))

v = u % q
print("U mod Q = " + str(v))

print("U.is_gcd_one(Q) = " + str(u.is_gcd_one(q))) 

w = Pol([Unit(1, 9)])
print("W = " + str(w))
print("W.is_gcd_one(Q) = " + str(w.is_gcd_one(q)))

