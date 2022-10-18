from optimization.utils.lib import *

from optimization.excercises.two.newton1d.base import Excercise, T

class ND(Excercise):
    def __init__(self):
        super().__init__(0.5,2.5, 1000, 1e-9)

    def f(self, x):
        return 3*x**2+12/x**3-5

    def sf(self, x: Expr) -> Expr:
        return self.f(x)