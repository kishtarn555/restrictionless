import imp

from optimization.utils.lib import *
from typing import Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class MultiFunctionOpt(ABC):
    x_i : arr
    @abstractmethod
    def run(
        self, 
        onStep:Callable[[arr], None]
    )->arr:
        pass

    @abstractmethod
    def step(self, xs: arr) -> arr:
        pass

    def dimension(self):
        return self.x_i.size