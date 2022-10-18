
import math as m
import numpy.ma as n


def F(x, mu, s):
    return 0.5*(1+m.erf((x-mu)/(s*m.sqrt(2))  ))
if __name__ == "__main__":
    mu = 5644
    s = 1615
    a,b=4000,20000
    while (b-a > 1e-9):
        h=(a+b)/2
        if (1-F(h, mu, s) > 0.05):
            a=h
        else:
            b=h
    print(a)
    print(F(a,mu,s))
    
    
    input("Press a key to end...")