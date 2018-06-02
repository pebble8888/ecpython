#!/usr/bin/env python 

#%matplotlib inline 
import numpy as np
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def desc(self):
        if self.x == -1 and self.y == -1:
            return "O"
        return "("+str(self.x)+","+str(self.y)+")"
    
    def is_equal(self, other):
        return self.x == other.x and self.y == other.y

    def is_equal_negative(self, other, prime):
        return self.x == other.x and - self.y == other.y - prime
        
    def iszero(self):
        return self.x == -1 and self.y == -1
    
    @staticmethod
    def zero():
        return Point(-1, -1)

class EC:
    def __init__(self, a, b, c, p):
        self.a = a
        self.b = b
        self.c = c
        self.p = p
        self.calc_order()
    
    def calc_order(self):
        self.points = []
        for x in range(self.p):
            for y in range(self.p):
                pt = Point(x,y)
                if self.oncurve(pt):
                    self.points.append(pt)
        self.points_count = len(self.points)
        self.order = len(self.points)+1

    def oncurve(self, pt):
        l = ((pt.y**2) % self.p)
        r = ((pt.x**3) + self.a*(pt.x**2) + self.b*pt.x + self.c) % self.p
        return l == r

    def d(self):
        return -4*(self.a**3)*self.c \
                + (self.a**2)*(self.b**2) \
                + 18*self.a*self.b*self.c \
                - 4*(self.b**3) \
                - 27 * (self.c**2)
    
    def inverse(self, a):
        assert self.p >= 2
        return a ** (self.p-2)
    
    def plus(self, p1, p2):
        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y
        if (p1.iszero()):
            return p2
        if (p2.iszero()):
            return p1
        
        if p1.is_equal_negative(p2, self.p):
            return Point.zero()
        
        elif p1.is_equal(p2):
            if (y1 == 0):
                return Point.zero()
            else:
                lm = (3 * (x1 **2) + 2 * self.a * x1 + self.b) * self.inverse(2 * y1)
                x3 = (lm ** 2) - self.a - x1 - x2
                y3 = - lm *(x3-x1) - y1
        else:
            lm = (y2-y1) * self.inverse(x2-x1)
            x3 = (lm ** 2) - self.a - x1 - x2
            y3 = -(lm*(x3-x1) + y1)

        q = Point(x3 , y3)
        q2 = Point(x3 % self.p, y3 % self.p)
        if not self.oncurve(q2):
            print("p1 {0} p2 {1} q {2} q2 {3}".format(p1.desc(), p2.desc(), q.desc(), q2.desc()))
            assert False
        return q2

    def mul(self, p, n):
        q = p
        for i in range(n-1):
            q = ec.plus(q, p)
        return q

ec = EC(0, 0, 7, 31)

print( "F" + str(ec.p) )
#print( "d:" + str(ec.d()) )
print( "#EC:" + str(ec.order) )
print( "" )

plotx = [p.x for p in ec.points]
ploty = [p.y for p in ec.points]
n = ["P"+str(i+1) for (i, p) in zip(range(len(ec.points)), ec.points)]

for i in range(ec.points_count):
    baseP = ec.points[i]
    print( "P"+str(i+1)+":" + baseP.desc() )
    for j in range(2, ec.order+1):
        p = ec.mul(baseP, j)
        print( str(j)+"*P"+str(i+1)+":"+p.desc() )
        if p.iszero():
            print("order:{0}".format(j))
            print("")
        if (p == baseP):
            print("")
            break
    
fig, ax = plt.subplots()
ax.scatter(plotx, ploty)

for i, txt in enumerate(n):
    ax.annotate(txt, (plotx[i],ploty[i]))
