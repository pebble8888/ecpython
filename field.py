#!/usr/bin/env python3

class F:
    def __init__(self, p, v):
        self.p = p
        self.v = v
        self.normalize()

    def normalize(self):
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

    def __floordiv__(self, other):
        assert(self.p == other.p)
        return F(self.p, self.v * (other.v ** (self.p-2)))

    def __mod__(self, other):
        assert(self.p == other.p)
        return F(self.p, self.v % other.v)

    def iszero(self):
        return self.v == 0

    def __str__(self):
        return str(self.v) 

