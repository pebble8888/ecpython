#!/usr/bin/env python3 

import numpy as np
import matplotlib.pyplot as plt
from ec import EC
from ec import Point

gp = 11
ec = EC(-7, 6, gp)

print("F" + str(ec.p))
print("#EC:" + str(ec.order))
print("")

plotx = [p.x.v for p in ec.points]
ploty = [p.y.v for p in ec.points]
n = ["P"+str(i+1) for (i, p) in zip(range(len(ec.points)), ec.points)]

for i in range(ec.points_count):
    baseP = ec.points[i]
    print( "P"+str(i+1)+":" + str(baseP) )
    for j in range(2, ec.order+1):
        p = ec.mul(baseP, j)
        print( str(j)+"*P"+str(i+1)+":"+str(p) )
        if p.isinf():
            print("order:{0}".format(j))
            print("")
        if p == baseP:
            print("")
            break

for i in range(ec.points_count):
    for j in range(i, ec.points_count):
        pt1 = ec.points[i]
        pt2 = ec.points[j]
        pt3 = ec.plus(pt1, pt2)
        index = -1
        for k in range(ec.points_count):
            if ec.points[k] == pt3:
                index = k
                break
        if index == -1:
            s = "O"
        else:
            s = "P"+str(index+1) 
        print("P"+str(i+1) + "+P"+str(j+1)+"="+s)
    
fig, ax = plt.subplots()
ax.scatter(plotx, ploty)

for i, txt in enumerate(n):
    ax.annotate(txt, (plotx[i],ploty[i]))

plt.show()
