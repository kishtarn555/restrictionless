from typing import List
from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import Xn
from optimization.excercises.two.newton1d.base import Excercise as ExcNew1D
from optimization.excercises.two.secant.base import Excercise as ExcSec
from optimization.restrictionless.newton import Newton

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

class Ej7Newton:
    def __init__(self):        
        self.x_i = arr([3,1,2,2])
    
    def fk(self,x1,x2,x3,x4):
        return (
            (100*(x2-x1**2))**2
            + (1-x1)**2
            + 90*(x4-x3**2)**2
            + (1-x3)**2 
            + 10.1*((x2-1)**2+(x4-1)**2) 
            + 19.8*(x2-1)*(x4-1)
        )
        
    def step(self, x, pts:List[np.ndarray]):
        print(f"x_{len(pts)} : {x}")
        pts.append(x)
        
    def run(self):
        exp = self.fk(Xn(0), Xn(1), Xn(2), Xn(3)) 
        newt = Newton(self.x_i, 1e-9, 1e-9, 1, exp)
        
        points =[newt.x_i]
        
        print(f"x_{0} : {newt.x_i}")
        x = newt.run(lambda x: self.step(x, points))
        print (f"Termino en {len(points)-1} pasos:")        
        return x

