from optimization.utils.lib import *

from optimization.excercises.two.newton1d.base import Excercise, T

class NC(Excercise):
    def __init__(self):
        super().__init__(0,3, 1000, 1e-9)

    def f(self, x):
        return 2*(x-3)**2+np.e**(0.5*x**2)

    def sf(self, x: Expr) -> Expr:
        return self.f(x)