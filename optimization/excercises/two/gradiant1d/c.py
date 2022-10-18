from optimization.utils.lib import *

from optimization.excercises.two.gradiant1d.base import Excercise1D, T

class GraC(Excercise1D):
    def __init__(self):
        super().__init__(
            2,
            0.05,
            1000,
            1e-9,
            1e-9,
            0,
            3
        )

    def f(self, x):
        return 2*(x - 3)**2 + np.e**(0.5*x**2)

    def sf(self, x):
        return self.f(x)