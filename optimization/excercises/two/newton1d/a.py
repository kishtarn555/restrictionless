from optimization.utils.lib import *

from optimization.excercises.two.newton1d.base import Excercise, T

class NA(Excercise):
    def __init__(self):
        super().__init__(0,4, 1000, 1e-9)

    def f(self, x):
        return 3*x**4+(x-1)**2

    def sf(self, x):
        return self.f(x)