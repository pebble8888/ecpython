#!/usr/bin/env python 

from ec import EC
from ec import Point

ec = EC(0,0,7, 31)

print("F" + str(ec.p))
print("#E:" + str(ec.order))


