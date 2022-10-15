from optimization.utils.lib import *

from optimization.utils.sm.vectorfunc import Xn
from optimization.excercises.two.gradiant.base import GradiantExcercise

class GradiantExcE(GradiantExcercise):

    def __init__(self):
        super().__init__(
            self.fk(Xn(0),Xn(1),Xn(2)),
            arr([0.155,0.155,0.155])
        )        
        self.delta=0.01

    def fk(self, x1, x2, x3):
        return (
            x1**4- 16*x1**2+ 5*x1
          + x2**4- 16*x2**2+ 5*x2
          + x3**4- 16*x3**2+ 5*x3
        )