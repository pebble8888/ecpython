#!/usr/bin/env python

ps = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

for p in ps:
    print("p {0}".format(p))
    print("(p-1)%3 {0}".format((p-1) % 3))
    l = []
    for x in range(1, p):
        a = (x**3) % p
        l.append(a)
    print(l)
    print(sorted(l))
    print("")

