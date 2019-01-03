#!/usr/bin/env python3

import operator
from field import F 
import copy
import sympy as sy
import unittest
import sys
from functools import lru_cache

class Pol:
    def __init__(self, units):
        self.units = units
        self.normalize()

    def sort(self):
        self.units.sort(key=operator.attrgetter("xpower", "ypower"), reverse=True)

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
        for i in l_units:
            i.normalize()
        self.units = []
        for x in l_units:
            if type(x.coef) is F:
                if not x.coef.iszero():
                    self.units.append(x)
            else:
                if x.coef != 0:
                    self.units.append(x)

    def ec_reduction(self, a, b):
        t = Pol.zero()
        for u in self.units:
            if u.ypower >= 2:
                yy = u.ypower // 2
                e = Pol([u]) // Pol([Unit(1, 0, 2*yy)])
                e = e * (Pol([Unit(1, 3, 0), Unit(a, 1, 0), Unit(b, 0, 0)]) ** yy)
            else:
                e = Pol([u])
            t.add(e)

        t.normalize()
        return t

    def highestUnitX(self):
        unit = Unit(0, 0, 0) 
        for u in self.units:
            if unit.xpower < u.xpower:
                unit = u
        return unit

    def __add__(self, other):
        self.units.extend(other.units)  
        self.normalize()
        return self

    def add(self, other):
        self.units.extend(other.units)
        return self
    
    def __sub__(self, other):
        for i in other.units:
            self.units.append(-i)
        self.normalize()
        return self

    def __mul__(self, other):
        l_units = []
        for i in self.units:
            for j in other.units:
                l_units.append(i * j)
        return Pol(l_units)

    #@lru_cache()
    def __pow__(self, other):
        assert(other != 0)
        m = copy.copy(self)
        for i in range(other-1):
            m = m * self
            m.normalize()
            #print(":", end="")
            #sys.stdout.flush()
        m.normalize()
        return m 
        """
        if other == 1:
            return self 
        elif other == 2:
            m = copy.copy(self)
            m = m * self
            m.normalize()
            return m
        m = copy.copy(self)
        if other % 2 == 0:
            n = other // 2 
            m = (m ** n) ** 2
        else:
            n = other // 2
            m = ((m ** n) ** 2) * self 
        m.normalize()
        return m
        """

    def __floordiv__(self, other):
        if len(other.units) == 0:
            assert(False)
        elif len(other.units) == 1:
            l_units = [] 
            for i in self.units:
                l_units.append(i // other.units[0])
            return Pol(l_units)
        else:
            assert(False) 

    def __mod__(self, other):
        assert(not self.hasY())
        assert(not other.hasY())
        o_h = other.highestUnitX()
        tmp = Pol(self.units)
        while True:
            tmp_h = tmp.highestUnitX()
            if tmp_h.xpower < o_h.xpower:
                break
            q = Pol([Unit(tmp_h.coef // o_h.coef, tmp_h.xpower - o_h.xpower, 0)])
            tmp = tmp - q * other
            #tmp.normalize()
            #print(".", end="")
            #sys.stdout.flush()
        return tmp

    def __neg__(self):
        l_units = []
        for i in self.units:
            l_units.append(-i)
        return Pol(l_units)

    def __eq__(self, other):
        if len(self.units) != len(other.units):
            return False
        for i in range(0, len(self.units)):
            if self.units[i] != other.units[i]:
                return False
        return True

    def iszero(self):
        return len(self.units) == 0

    def is_gcd_one(self, other):
        s = self.highestUnitX()
        o = other.highestUnitX()
        if s.xpower < o.xpower:
            m = copy.deepcopy(other) % self 
            return not m.iszero()
        m = self % other
        return not m.iszero()

    def hasY(self):
        for u in self.units:
            if not u.ypower == 0:
                return True
        return False

    def toField(self, prime):
        l_units = []
        for u in self.units:
            l_units.append(u.toField(prime))
        return Pol(l_units)

    def toFrob(self, n):
        l_units = []
        for u in self.units:
            l_units.append(u.toFrob(n))
        return Pol(l_units)

    def toYPower(self, n):
        l_units = []
        for u in self.units:
            l_units.append(u.toYPower(n))
        return Pol(l_units)

    def __str__(self):
        self.sort()
        if self.iszero():
            return "0"
        s = ""
        for u in self.units:
            s += " + " + str(u)  
        return s.strip(" + ")

    @staticmethod
    def zero():
        return Pol([])

class Unit:
    def __init__(self, coef, xpower, ypower): 
        self.coef = coef
        self.xpower = xpower
        self.ypower = ypower

    def normalize(self):
        if type(self.coef) is F:
            self.coef.normalize()

    def __str__(self):
        if self.xpower == 0 and self.ypower == 0:
            return str(self.coef)
        if type(self.coef) is F:
            if self.coef.iszero():
                return ""
        else:
            if type(self.coef) is F:
                if self.coef.iszero():
                    return ""
            else:
                if self.coef == 0:
                    return ""

        if type(self.coef) is F:
            if self.coef.isone():
                s = ""
            elif (-self.coef).isone():
                s = "-"
            else:
                s = str(self.coef) 
        else:
            if self.coef == 1:
                s = ""
            elif self.coef == -1:
                s = "-"
            else:
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
            return Unit(self.coef + other.coef, self.xpower, self.ypower)
        return [self, other]

    def __sub__(self, other):
        if self.xpower == other.xpower and self.ypower == other.ypower:
            return Unit(self.coef - other.coef, self.xpower, self.ypower)
        return [self, -other]

    def __neg__(self):
        return Unit(-self.coef, self.xpower, self.ypower)

    def __mul__(self, other):
        return Unit(self.coef * other.coef, self.xpower + other.xpower, self.ypower + other.ypower)

    def __floordiv__(self, other):
        return Unit(self.coef // other.coef, self.xpower - other.xpower, self.ypower - other.ypower)

    def __eq__(self, other):
        return self.coef == other.coef and self.xpower == other.xpower and self.ypower == other.ypower

    def iszero(self):
        return self.coef.iszero()

    def toField(self, prime):
        return Unit(F(prime, self.coef), self.xpower, self.ypower)      

    def toFrob(self, n):
        return Unit(self.coef, self.xpower * n, self.ypower * n) 

    @staticmethod
    def zero(prime):
        return Pol(prime, [])

# test for Unit
class TestUnit(unittest.TestCase):
    def test_add(self):
        actual = Unit(1,1,1) + Unit(1,1,1)
        expect = Unit(2,1,1)
        self.assertEqual(actual, expect)

    def test_sub(self):
        actual = Unit(4,1,1) - Unit(1,1,1)
        expect = Unit(3,1,1)
        self.assertEqual(actual, expect)

    def test_mul(self):
        actual = Unit(1,1,1) * Unit(1,1,1)
        expect = Unit(1,2,2)
        self.assertEqual(actual, expect)

    def test_floordiv(self):
        actual = Unit(5,1,1).toField(19) // Unit(2,1,1).toField(19)
        expect = Unit(12,0,0).toField(19)
        self.assertEqual(actual, expect)

    def test_toFrob(self):
        actual = Unit(2, 3, 0).toFrob(2)
        expect = Unit(2, 6, 0)
        self.assertEqual(actual, expect)

    def test_toFrob(self):
        actual = Unit(2, 0, 3).toFrob(2)
        expect = Unit(2, 0, 6)
        self.assertEqual(actual, expect)

    def test_toFrob(self):
        actual = Unit(4, 1, 1).toFrob(2)
        expect = Unit(4, 2, 2)
        self.assertEqual(actual, expect)

# test for Pol
class TestPol(unittest.TestCase):
    def test_add(self):
        actual = Pol([Unit(1,1,1)]) + Pol([Unit(1,1,1)])
        expect = Pol([Unit(2,1,1)])
        self.assertEqual(actual, expect)

    def test_neg(self):
        actual = - Pol([Unit(2,1,1)])
        expect = Pol([Unit(-2,1,1)])
        self.assertEqual(actual, expect)

    def test_mul1(self):
        actual = Pol([Unit(1,3,0), Unit(1,0,0)]) * Pol([Unit(1,3,0), Unit(1,0,0)])
        expect = Pol([Unit(1,6,0), Unit(2,3,0), Unit(1,0,0)])
        self.assertEqual(actual, expect)

    def test_mul2(self):
        actual = Pol([Unit(2,0,0)]) * Pol([Unit(1,3,0)])
        expect = Pol([Unit(2,3,0)])
        self.assertEqual(actual, expect)
    
    def test_pow(self):
        actual = Pol([Unit(1,3,0), Unit(1,0,0)]) ** 2
        expect = Pol([Unit(1,6,0), Unit(2,3,0), Unit(1,0,0)])
        self.assertEqual(actual, expect)

    def test_pow3(self):
        actual = Pol([Unit(1,3,1), Unit(1,0,1)]) ** 3
        expect = Pol([Unit(1,9,3), Unit(3,6,3), Unit(3,3,3), Unit(1,0,3)])
        self.assertEqual(actual, expect)

    def test_reduction(self):
        actual = Pol([Unit(1,0,3)]).ec_reduction(2, 1)
        expect = Pol([Unit(1,3,1), Unit(2,1,1), Unit(1,0,1)])
        self.assertEqual(actual, expect)

    def test_reduction(self):
        actual = Pol([Unit(1,0,4)]).ec_reduction(2, 1)
        expect = Pol([Unit(1,3,0), Unit(2,1,0), Unit(1,0,0)]) ** 2
        self.assertEqual(actual, expect)

    def test_hoge(self):
        """
        q = 19
        x = Pol([Unit(F(q, 2), 5, 0), Unit(F(q, -1), 1, 0)])
        print("X=" + str(x))

        y = Pol([Unit(F(q, 3), 3, 0), Unit(F(q, 2), 1, 0), Unit(F(q, 1), 0, 0)])
        print("Y=" + str(y))

        z = x ** 2
        print("Z=" + str(z))

        xy = x % y
        print("X mod Y =" + str(xy))

        r = Pol([Unit(F(q, 3), 3, 2), Unit(F(q, 5), 0, 1)])
        print("R=" + str(r))

        s = Pol([Unit(F(q, 2), 1, 1), Unit(F(q, 1), 0, 0)])
        print("S=" + str(s))

        rs = r * s
        print("R*S =" + str(rs))
        """

        #print(str(p.is_gcd_one(r)))
        #print(str(r.is_gcd_one(p)))

if __name__ == '__main__':
    unittest.main()

