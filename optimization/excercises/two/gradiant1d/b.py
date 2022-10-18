from optimization.utils.lib import *

from optimization.excercises.two.gradiant1d.base import Excercise1D, T

class GraB(Excercise1D):
    def __init__(self):
        super().__init__(
            3,
            0.05,
            1000,
            1e-9,
            1e-9,
            0,
            np.pi
        )

    def f(self, x):
        return -4*x*np.sin(x)

    def sf(self, x):
        return -4*x*sp.sin(x)