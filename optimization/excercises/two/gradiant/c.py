from optimization.utils.lib import *

from optimization.utils.sm.vectorfunc import Xn
from optimization.excercises.two.gradiant.exc_2d import Excercise2D

class GradiantExcC(Excercise2D):

    def __init__(self):
        super().__init__(
            self.fk(Xn(0),Xn(1)),
            arr([9,2]),
            0.5,
            10,
            0.5,
            10,
            0,
            10
        )

    def fk(self, x1, x2):
        return 0.1*(12+x1**2+(1+x1**2)/(x1**2)+(100+x1**2*x2**2)/(x1*x2)**4)