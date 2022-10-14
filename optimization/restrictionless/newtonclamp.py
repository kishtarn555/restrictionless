from optimization.utils.lib import *
from optimization.restrictionless.newton import Newton

class NewtonClamped(Newton):
    minima: arr
    maxima: arr
    def step(self, x: arr) -> arr:
        return np.max(
            np.min(super().step(x), self.maxima),
            self.maxima,
        )