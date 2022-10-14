from typing import List

from optimization.restrictionless.newton import Newton
from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import get_lambda, Xn
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


class ExcD:
    
        
    def main(self)->None:
        e= Xn(0)**3+Xn(1)**2+Xn(2)
        print(e)
        ntw =  Newton(np.array([1.0,-1.0,1.0]), 1e-9, 1e-9,0.05, e)
        points =[]
        x= ntw.run( lambda x: points.append(np.copy(x)))
        print (f"Finished on {len(points)} steps:")
        print(f"x={x}")
        print(f"f({x})={get_lambda(e, x.size)(*x)}")
        
        