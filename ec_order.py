#!/usr/bin/env python 

import sys
from ec import EC
from ec import Point
import sympy as sy

idx = int(sys.argv[1])
p = sy.prime(idx)

ec = EC(0, 0, 7, p)

print("F" + str(ec.p))
print("#EC:" + str(ec.order))
