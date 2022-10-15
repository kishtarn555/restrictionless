from typing import Any, Callable

from abc import ABC, abstractmethod

class StepAlgorithm(ABC):
    @abstractmethod
    def run(self, onStep:Callable[[float], None]) -> float:
        pass

    @abstractmethod
    def step(self, x: float) -> float:
        pass 