from optimization.utils.lib import *

from optimization.excercises.two.gradiant1d.base import Excercise1D, T

class GraA(Excercise1D):
    def __init__(self):
        super().__init__(
            3,
            0.005,
            1000,
            1e-9,
            1e-9,
            0,
            4
        )

    def f(self, x: T):
        return 3*x**4+(x-1)**2

    def sf(self, x):
        return self.f(x)