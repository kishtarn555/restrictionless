from typing import List

from abc import ABC
from dataclasses import dataclass

from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import get_lambda
from optimization.restrictionless.gradient import GradientDescent

@dataclass
class GradiantExcercise(ABC):
    expr: Expr
    x_i: arr

    def run(self) -> List[arr]:
        gr = GradientDescent(self.x_i, self.expr, 0.00005, 1000, 1e-6, 1e-6)
        points = []
        x=gr.run(lambda x: points.append(x))
        print(f"Finished on {len(points)} steps")
        print(f"optimum x = {x}")
        print(f"f(x)= {get_lambda(self.expr, x.size)(*x)}")
        return points

