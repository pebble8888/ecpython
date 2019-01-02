#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from polynomial import Pol 
from polynomial import Unit
from field import F
import copy

class Point:
    # x, y is Field
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        if self.x.isinf() and self.y.isinf():
            return "O"
        return "("+str(self.x)+","+str(self.y)+")"
    
    def is_equal_negative(self, other):
        return self.x == other.x and self.y == - other.y
        
    def isinf(self):
        return self.x.isinf() and self.y.isinf()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y 

    def __ne__(self, other):
        return not self.__eq__(other)
    
    @staticmethod
    def inf(prime):
        return Point(F(prime, None), F(prime, None))

class EC:
    # y^2 = x^3 + a * x + b
    # mod p
    # a, b, p: int
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        self.calc_order()
    
    def calc_order(self):
        self.points = []
        for x in range(self.p):
            for y in range(self.p):
                pt = Point(F(self.p, x),F(self.p, y))
                if self.oncurve(pt):
                    self.points.append(pt)
        self.points_count = len(self.points)
        self.order = len(self.points)+1

    def oncurve(self, pt):
        l = pt.y.v**2
        r = pt.x.v**3 + self.a *pt.x.v + self.b
        return F(self.p, l) == F(self.p, r)
    
    def inverse(self, a):
        assert self.p >= 2
        return a ** (self.p-2)
    
    def plus(self, p1, p2):
        if p1.isinf():
            return p2
        if p2.isinf():
            return p1

        x1 = p1.x.v
        y1 = p1.y.v
        x2 = p2.x.v
        y2 = p2.y.v
        if p1.is_equal_negative(p2):
            return Point.inf(self.p)
        elif p1 == p2:
            if y1 == 0:
                return Point.inf(self.p)
            else:
                lm = (3 * (x1 **2) + self.a) * self.inverse(2 * y1)
                x3 = lm ** 2 - x1 - x2
                y3 = - lm *(x3-x1) - y1
        else:
            lm = (y2-y1) * self.inverse(x2-x1)
            x3 = lm ** 2 - x1 - x2
            y3 = -(lm*(x3-x1) + y1)

        q = Point(F(self.p, x3), F(self.p, y3))
        if not self.oncurve(q):
            print("q=" + str(q))
            assert False
        return q

    def mul(self, pt, n):
        t_pt = pt
        for i in range(n-1):
            t_pt = self.plus(t_pt, pt)
        return t_pt

    def psi(self, n):
        assert(n >= 0)
        if n == 0:
            return Pol.zero()
        elif n == 1:
            return Pol([Unit(1, 0, 0)])
        elif n == 2:
            return Pol([Unit(2, 0, 1)])
        elif n == 3:
            return Pol([Unit(3, 4, 0), \
                        Unit(6 * self.a, 2, 0), \
                        Unit(12 * self.b, 1, 0), \
                        Unit(- self.a ** 2, 0, 0)]) 
        elif n == 4:
            return Pol([Unit(4, 0, 1)]) * \
                   Pol([Unit(1, 6, 0), \
                        Unit(5 * self.a, 4, 0), \
                        Unit(20 * self.b, 3, 0), \
                        Unit(-5 * (self.a **2), 2, 0), \
                        Unit(-4 * self.a * self.b, 1, 0), \
                        Unit(-8 * (self.b ** 2) - (self.a ** 3), 0, 0)])
        elif n % 2 == 1:
            m = (n-1)//2
            e = self.psi(m+2)
            f = self.psi(m) ** 3
            g = self.psi(m-1)
            h = self.psi(m+1) ** 3
            r = e*f - g*h
            return r.ec_reduction(self.a, self.b)
            #return r
        else:
            m = n//2
            e = self.psi(m+2) 
            f = self.psi(m-1) ** 2
            g = self.psi(m-2)
            h = self.psi(m+1) ** 2
            i = self.psi(m) * (e*f - g*h)
            r = i // Pol([Unit(2, 0, 1)])
            return r.ec_reduction(self.a, self.b)
            #return r

    def phi(self, n):
        assert(n >= 1)
        r = Pol([Unit(1, 1, 0)]) * (self.psi(n) ** 2) - self.psi(n+1) * self.psi(n-1)
        return r.ec_reduction(self.a, self.b)
        #return r

    def omega(self, n):
        assert(n >= 1)
        if n == 1:
            return Pol([Unit(1, 0, 1)])
        else:
            r = (self.psi(n+2) * (self.psi(n-1) ** 2) - self.psi(n-2) * (self.psi(n+1) ** 2)) // Pol([Unit(4, 0, 1)])
            #return r
            return r.ec_reduction(self.a, self.b)

    def omega_yminus(self, n):
        return self.omega(n) // Pol([Unit(1, 0, 1)])

    def __str__(self):
        return "EC(" + str(self.a) + "," + str(self.b) + "," + str(self.p) + ")" 

if __name__ == '__main__':
    ec = EC(2, 1, 19)
    for i in range(6):
        print(ec.psi(i))
    print("")
    for i in range(1, 6):
        print(ec.phi(i))
    print("")
    for i in range(1, 6):
        print(ec.omega(i))

    """
    # l = 2
    q = 19
    c = Pol([Unit(F(q, 1), q, 0), Unit(F(q, -1), 1, 0)]) 
    d = Pol([Unit(F(q, 1), 3, 0), Unit(F(q, 2), 1, 0), Unit(F(q, 1), 0, 0)])
    e = c.is_gcd_one(d)
    print("c:"+str(c) + ",d:"+str(d)+",is_gcd_one:"+str(e))
    """

