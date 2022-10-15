from optimization.utils.lib import *

from optimization.utils.sm.vectorfunc import Xn
from optimization.excercises.two.gradiant.base import GradiantExcerciseClamped

class GradiantExcD(GradiantExcerciseClamped):

    def __init__(self):
        super().__init__(
            self.fk(Xn(0),Xn(1),Xn(2)),
            arr([1,1,1]),
            arr([-2, -2,-2]),
            arr([2, 2, 2])
        )        
        self.delta=0.1

    def fk(self, x1, x2, x3):
        return x1**3+x2**2+x3