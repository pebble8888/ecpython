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
            e = copy.deepcopy(self).psi(m+2) 
            f = copy.deepcopy(self).psi(m).power(3)
            g = copy.deepcopy(self).psi(m-1)
            h = copy.deepcopy(self).psi(m+1).power(3)
            #print("e="+str(e))
            #print("f="+str(f))
            #print("g="+str(g))
            #print("h="+str(h))
            r = e*f - g*h
            return r.ec_reduction(self.a, self.b)
        else:
            m = n//2
            e = copy.deepcopy(self).psi(m+2) 
            f = copy.deepcopy(self).psi(m-1).power(2)
            g = copy.deepcopy(self).psi(m-2)
            h = copy.deepcopy(self).psi(m+1).power(2)
            #print("e="+str(e))
            #print("f="+str(f))
            #print("g="+str(g))
            #print("h="+str(h))
            i = copy.deepcopy(self).psi(m) * (e*f - g*h)
            r = i // Pol([Unit(2, 0, 1)])
            return r.ec_reduction(self.a, self.b)

    def phi(self, n):
        assert(n >= 0)

    def omega(self, n):
        assert(n >= 0)

if __name__ == '__main__':
    """
    gp = 11
    ec = EC(-7, 6, gp)

    print("F" + str(ec.p))
    m3 = ec.p % 3
    print("p mod 3 is " + str(m3))
    print("#E:" + str(ec.order))
    print("")

    for i in range(1, ec.order+1):
        print(str(i) + " torsion Point:")
        for j in range(ec.points_count):
            pt = ec.mul(ec.points[j], i)
            if pt.isinf():
                print(" P" + str(j+1))

    plotx = [pt.x.v for pt in ec.points]
    ploty = [pt.y.v for pt in ec.points]
    n = ["P"+str(i+1) for (i, p) in zip(range(len(ec.points)), ec.points)]

    for i in range(ec.points_count):
        baseP = ec.points[i]
        for j in range(2, ec.order+1):
            pt = ec.mul(baseP, j)
            if pt.isinf():
                zz = 0
            if pt == baseP:
                break
        
    fig, ax = plt.subplots()
    ax.scatter(plotx, ploty)

    for i, txt in enumerate(n):
        ax.annotate(txt, (plotx[i],ploty[i]))

    #plt.show()
    """

    #ec = EC(-7, 6, 19)
    ec = EC(1, 1, 19)
    print(ec.psi(0))
    print(ec.psi(1))
    print(ec.psi(2))
    print(ec.psi(3))
    print(ec.psi(4))
    print(ec.psi(5))
    print(ec.psi(6))
