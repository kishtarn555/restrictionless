from optimization.utils.lib import *

from optimization.utils.sm.vectorfunc import Xn
from optimization.excercises.two.gradiant.exc_2d import Excercise2D

class GradiantExcA(Excercise2D):

    def __init__(self):
        super().__init__(
            self.fk(Xn(0),Xn(1)),
            arr([4,-4]),
            -5,
            5,
            -5,
            5,
            0,
            40000
        )

    def fk(self, x1, x2):
        return 100*(x2-x1**2)**2+(1-x1)**2