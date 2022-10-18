from optimization.utils.lib import *

from optimization.excercises.two.gradiant1d.base import Excercise1D, T

class GraD(Excercise1D):
    def __init__(self):
        super().__init__(
            2,
            0.05,
            1000,
            1e-9,
            1e-9,
            0.5,
            2.5
        )

    def f(self, x):
        return 3*x**2+12/x**3-5

    def sf(self, x):
        return self.f(x)