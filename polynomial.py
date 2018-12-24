#!/usr/bin/env python3

import operator
from field import F 

class Pol:
    def __init__(self, p, units):
        self.p = p
        self.units = units
        self.normalize()

    def normalize(self):
        l_units = []
        for u in self.units:
            found = False
            for l_u in l_units:
                if u.xpower == l_u.xpower and u.ypower == l_u.ypower:
                    l_u.coef += u.coef
                    found = True
                    break
            if not found:
                l_units.append(u)
        self.units = [x for x in l_units if not x.coef.iszero()]
        self.units.sort(key=operator.attrgetter('xpower'), reverse=True)

    def highestUnitX(self):
        unit = Unit(F(self.p, 0), 0, 0) 
        for u in self.units:
            if unit.xpower < u.xpower:
                unit = u
        return unit

    def __add__(self, other):
        l_units = self.units
        l_units.extend(other.units)  
        return Pol(self.p, l_units)
    
    def __sub__(self, other):
        l_units = self.units
        for i in other.units:
            l_units.append(-i)
        return Pol(self.p, l_units)

    def __mul__(self, other):
        l_units = []
        for i in self.units:
            for j in other.units:
                l_units.append(i * j)
        return Pol(self.p, l_units)

    def __mod__(self, other):
        assert(not self.hasY())
        assert(not other.hasY())
        o_h = other.highestUnitX()
        tmp = self
        while True:
            tmp_h = tmp.highestUnitX()
            if tmp_h.xpower < o_h.xpower:
                break
            p = Pol(self.p, [Unit(tmp_h.coef // o_h.coef, tmp_h.xpower - o_h.xpower, 0)])
            tmp = tmp - p * other
        return tmp

    def iszero(self):
        return len(self.units) == 0

    def is_gcd_one(self, other):
        return (self % other).iszero()

    def hasY(self):
        for u in self.units:
            if not u.ypower == 0:
                return True
        return False

    def __str__(self):
        if self.iszero():
            return "0"
        s = ""
        for u in self.units:
            s += " + " + str(u)  
        return s.strip(" + ")

class Unit:
    def __init__(self, coef, xpower, ypower): 
        self.coef = coef
        self.xpower = xpower
        self.ypower = ypower

    def __str__(self):
        if self.xpower == 0 and self.ypower == 0:
            return str(self.coef)
        if self.coef.iszero():
            return ""
        s = str(self.coef) 
        if self.xpower == 1:
            s += "x"
        elif self.xpower > 1:
            s += "x^"+str(self.xpower)
        if self.ypower == 1:
            s += "y"
        elif self.ypower > 1:
            s += "y^"+str(self.ypower)
        return s

    def __add__(self, other):
        if self.xpower == other.xpower and self.ypower == other.ypower:
            return Unit(self.coef + other.coef, self.xpower)
        return [self, other]

    def __sub__(self, other):
        if self.xpower == other.xpower and self.ypower == other.ypower:
            return Unit(self.coef - other.coef, self.xpower, self.ypower)
        return [self, -other]

    def __neg__(self):
        return Unit(- self.coef, self.xpower, self.ypower) 

    def __mul__(self, other):
        return Unit(self.coef * other.coef, self.xpower + other.xpower, self.ypower + other.ypower)

    def __floordiv__(self, other):
        return Unit(self.coef // other.coef, self.xpower - other.xpower, self.ypower - other.ypower)

    def iszero(self):
        return self.coef.iszero()

if __name__ == '__main__':

    #d = lcm(2, 3)
    #print(d)

    #u = Unit(3, 2)
    #print(u)

    p = Pol(19, [Unit(F(19, 2), 5, 0), Unit(F(19, -1), 1, 0)])
    print("P=" + str(p))

    q = Pol(19, [Unit(F(19, 3), 3, 0), Unit(F(19, 2), 1, 0), Unit(F(19, 1), 0, 0)])
    print("Q=" + str(q))

    v = p % q
    print("P mod Q =" + str(v))

    r = Pol(19, [Unit(F(19, 3), 3, 2), Unit(F(19, 5), 0, 1)])
    print("R=" + str(r))

    s = Pol(19, [Unit(F(19, 2), 1, 1), Unit(F(19, 1), 0, 0)])
    print("S=" + str(s))

    x = r * s
    print("R * S =" + str(x))


