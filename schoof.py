#!/usr/bin/env python3

from polynomial import Pol
from ec import EC 
from polynomial import Pol 
from polynomial import Unit

if __name__ == '__main__':
    q = 19
    ec = EC(2, 1, q)

    for l in [3, 5]:
        print("l:" + str(l))
        ql = q % l
        if l >= q:
            break
        print("q:"+str(q)+" l:"+str(l) + " ql:"+str(ql))
        jmax = (l-1)//2
        print("j range:[1, "+str(jmax)+"]")
        found = False

        # (b) x'
        nn1 = ec.omega(ql);
        print("nn1:" + str(nn1))
        nn2 = Pol([Unit(1, 0, q **2)]) * (ec.psi(ql) ** 3) 
        print("nn2:" + str(nn2))
        n1 = (nn1 - nn2) ** 2
        print("n1:" + str(n1))
        n2 = - (ec.phi(ql) + Pol([Unit(1, q ** 2, 0)]) * (ec.psi(ql) ** 2))
        print("n2:" + str(n2))
        n3 = (ec.phi(ql) - Pol([Unit(1, q ** 2, 0)]) * (ec.psi(ql) ** 2)) ** 2
        print("n3:" + str(n3))
        b_num1 = n1 + n2 * n3;
        print("b_num1:" + str(b_num1))
        b_den1 = (ec.psi(ql) ** 2) * ((ec.phi(ql) - Pol([Unit(1, q ** 2, 0)]) * (ec.psi(ql) ** 2)) ** 2)
        print("b_den1:" + str(b_den1))

        for j in range(1, jmax + 1):
            print("j:"+str(j))
            # xj(q)
            num2 = ec.phi(j).toFrob(q)
            print("num2:" + str(num2))
            den2 = ec.psi(j).toFrob(q) ** 2
            print("den2:" + str(den2))
            p1 = b_num1 * den2 - num2 * b_den1
            p1 = p1.ec_reduction(ec.a, ec.b)
            p1 = p1.toField(q)
            p1 = p1 % ec.psi(l).toField(q)
            if p1.iszero():
                # to iii.
                found = True
                break
        if found:
            # iii
            print("x found")
            # y
            d = (ec.omega(ql) - Pol([Unit(1, 0, q ** 2)]) * (ec.psi(ql)**3))
            e = - ec.phi(ql) + Pol([Unit(2, q ** 2, 0)]) * (ec.psi(ql)**2)
            e = e.ec_reduction(ec.a, ec.b)
            f = ec.phi(ql) - Pol([Unit(1, q ** 2, 0)]) * (ec.psi(ql)**2)
            f = f.ec_reduction(ec.a, ec.b)
            num1 = d * (e * (f**2) - (d**2)) - Pol([Unit(1, 0, q **2)]) * (ec.psi(ql)**3) * (f**3)
            num1 = num1 * ec.psi(ql)
            den1 = (ec.psi(ql)**3) * (f**3) * ec.psi(ql)
            num2 = ec.omega(j).toFrob(q)
            den2 = ec.psi(j).toFrob(q) ** 3
            p1 = num1 * den2 - num2 * den1
            p2 = p1.ec_reduction(ec.a, ec.b)
            if p2.hasY():
                p3 = p2 // Pol([Unit(1, 0, 1)])
            else:
                p3 = p2
            p4 = p3.toField(q)
            psil = ec.psi(l).toField(q)
            print("psi("+str(l)+"):"+str(psil))
            p6 = p4 % psil
            print("pol % psi("+str(l)+"):"+str(p6))
            if p6.iszero():
                print("a = "+str(j)+" mod "+str(l)) 
            else:
                print("a = "+str(-j)+" mod "+str(l))
        else:
            # (d)
            found = False
            w = 1
            for i in range(1, l):
                if (i ** 2) % l == ql:
                    found = True
                    w = i
                    break
            if not found:
                print("a = 0 mod l because of w not found (d)")
            else:
                # (e) x
                p1 = Pol([Unit(1, q, 0)]) * (ec.psi(w) ** 2) - ec.phi(w)
                p2 = p1.ec_reduction(ec.a, ec.b)
                p3 = p2.toField(q)
                print(p3)
                p4 = p3 % ec.psi(l).toField(q)
                print(p4)
                if not p4.iszero():
                    print("a = 0 mod "+str(l)+" because of gcd = 1 (e)")
                else:
                    # (e) y
                    p5 = (Pol([Unit(1, 0, q)]) * (ec.psi(w) ** 3) - ec.omega(w)) // Pol([Unit(1, 0, 1)])
                    p6 = p5.ec_reduction(ec.a, ec.b)
                    p7 = p6.toField(q)
                    print(p7)
                    if p7.is_gcd_one(rc.psi(l).toField(q)):
                        print("a = "+str(-2*w) + " mod "+str(l))
                    else:
                        print("a = "+str(2*w) + " mod "+str(l))

