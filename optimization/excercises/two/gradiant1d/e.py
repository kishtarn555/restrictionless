from optimization.utils.lib import *

from optimization.excercises.two.gradiant1d.base import Excercise1D, T

class GraE(Excercise1D):
    def __init__(self):
        super().__init__(
            2,
            0.05,
            1000,
            1e-9,
            1e-9,
            1,
            5
        )

    def f(self, x):
        return 2*x**2+16/x

    def sf(self, x):
        return self.f(x)