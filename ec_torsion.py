#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from ec import EC
from ec import Point

gp = 19
ec = EC(2, 1, gp)

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

plt.show()
