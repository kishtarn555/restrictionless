
from typing import Callable
from dataclasses import dataclass

from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import get_lambda, Xn
from optimization.base.mfo import MultiFunctionOpt
from optimization.restrictionless.gradient import GradientDescent

def _min(a, b):
    if (a < b):
        return a
    return b

def _max(a, b):
    if (a > b):
        return a
    return b

@dataclass
class GradientDescentClamped(GradientDescent):
    minimum: arr
    maximum: arr
    
    def step(self, xs: arr) -> arr:
        xn = np.add(xs, -self.delta*self.gradient(xs)) # unclamped
        return arr(
            [
                _max(_min(e, self.maximum[i]), self.minimum[i]) # clamp
                for i, e in enumerate(xn)
            ]
        )
