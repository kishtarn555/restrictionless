from optimization.utils.lib import *

from optimization.excercises.two.newton1d.base import Excercise, T

class NE(Excercise):
    def __init__(self):
        super().__init__(1,5, 1000, 1e-9)

    def f(self, x):
        return 2*x**2+16/x

    def sf(self, x: Expr) -> Expr:
        return self.f(x)