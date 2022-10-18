from optimization.utils.lib import *
from typing import Callable

from dataclasses import dataclass

from optimization.base.lfo import StepAlgorithm

@dataclass
class Netwon1D(StepAlgorithm):    
    df: Callable[[float], float]
    df2: Callable[[float], float]
    x_i: float
    max_steps: int
    tolerance: float
    
    def run(self, onStep: Callable[[float], None]) -> float:
        steps:int=0
        x = self.x_i
        while (steps < self.max_steps):
            steps +=1
            px = x
            x= self.step(x)
            onStep(x)
            if (np.abs(px-x) < self.tolerance):
                break           
        return x

    def step(self, x: float) -> float:
        return x -self.df(x)/self.df2(x)

