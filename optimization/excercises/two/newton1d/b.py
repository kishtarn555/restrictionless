from optimization.utils.lib import *

from optimization.excercises.two.newton1d.base import Excercise, T

class NB(Excercise):
    def __init__(self):
        super().__init__(0,np.pi, 1000, 1e-9)

    def f(self, x):
        return -4.0*x*np.sin(x) 

    def sf(self, x: Expr) -> Expr:
        return -4.0*x*sp.sin(x)