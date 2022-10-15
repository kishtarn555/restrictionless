from typing import Type
from optimization.utils.lib import *
from typing import Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class MultiFunctionOpt(ABC):
    x_i : np.ndarray
    @abstractmethod
    def run(
        self, 
        onStep:Callable[[np.ndarray], None]
    )->np.ndarray:
        pass

    @abstractmethod
    def step(self, xs: np.ndarray) -> np.ndarray:
        pass

    def dimension(self):
        return self.x_i.size