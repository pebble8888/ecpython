#!/usr/bin/env python3

import unittest

class F:
    def __init__(self, p, v):
        self.p = p
        self.v = v
        self.normalize()

    def normalize(self):
        #if self.v is not None:
        self.v = self.v % self.p

    def __add__(self, other):
        assert(self.p == other.p)
        return F(self.p, self.v + other.v)

    def __sub__(self, other):
        assert(self.p == other.p)
        return F(self.p, self.v - other.v)

    def __neg__(self):
        return F(self.p, -self.v)

    def __mul__(self, other):
        assert(self.p == other.p)
        return F(self.p, self.v * other.v)

    def __pow__(self, other):
        return F(self.p, self.v ** other)

    def __floordiv__(self, other):
        assert(self.p == other.p)
        if self.v % other.v == 0:
            return F(self.p, self.v // other.v)
        return F(self.p, self.v * (other.v ** (self.p-2)))

    def __mod__(self, other):
        assert(self.p == other.p)
        return F(self.p, self.v % other.v)

    def iszero(self):
        return self.v == 0

    def isone(self):
        return self.v == 1

    def __str__(self):
        return str(self.v) 

    def __eq__(self, other):
        assert(self.p == other.p)
        return self.v == other.v

class TestField(unittest.TestCase):
    def test_divide(self):
        actual = F(3, 1) // F(3, 1)    
        expect = F(3, 1) 
        self.assertEqual(actual, expect)
    
if __name__ == '__main__':
    unittest.main()

