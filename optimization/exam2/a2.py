from typing import List
from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import Xn
from optimization.excercises.two.newton1d.base import Excercise, T

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

class Task2 (Excercise):

    def __init__(self):
        super().__init__(5, 15, 1000, 1e-9)

    def f(self, x):
        return 120+1.5*x+0.2/x*(1000)

    def sf(self, x: Expr) -> Expr:
        return self.f(x) # type: ignore