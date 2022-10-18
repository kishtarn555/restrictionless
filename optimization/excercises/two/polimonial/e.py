from optimization.utils.lib import *

from optimization.excercises.two.polimonial.base import Excercise, T

class PolE(Excercise):
    def __init__(self):
        super().__init__(1, 5, 1000, 1e-9, 5)

    def f(self, x):
        return 2*x**2+16/x

    def sf(self, x: Expr) -> Expr:
        return self.f(x)