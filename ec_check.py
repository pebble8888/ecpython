#!/usr/bin/env python 

import numpy as np
import matplotlib.pyplot as plt
from ec import EC
from ec import Point

ec = EC(0, 0, 7, 31)

print("F" + str(ec.p))
print("#EC:" + str(ec.order))
print("")

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

