from dataclasses import dataclass

from optimization.utils.lib import *
from optimization.restrictionless.newton import Newton

@dataclass
class NewtonClamped(Newton):
    minima: arr
    maxima: arr
    def min(self,a,b):
        if (a<b):
            return a
        return b
    def max(self,a,b):
        if (a>b):
            return a
        return b
    def step(self, x: arr) -> arr:
        tmp=super().step(x)
        return arr( 
            [
                self.max(self.min(tmp[i],self.maxima[i]),self.minima[i])
                for i in range(x.size) 
            ]        
        )