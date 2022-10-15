from typing import List

from abc import ABC
from dataclasses import dataclass

from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import get_lambda
from optimization.restrictionless.gradient import GradientDescent
from optimization.restrictionless.gradientclamped import GradientDescentClamped

@dataclass
class GradiantExcercise(ABC):
    expr: Expr
    x_i: np.ndarray

    def run(self) -> List[np.ndarray]:
        e1=1e-9
        e2=1e-9
        print(f"Punto inical: {self.x_i}")
        print(f"Razon de aprendizaje: {self.delta}")  # type: ignore # self.detla is created dynamically bc I was lazy
        print(f"Precision para dif. de pasos: {e1}")
        print(f"Precision en la pendiente: {e2}")
        gr = GradientDescent(self.x_i, self.expr, self.delta, 1000, e1, e2) # type: ignore 
        points = []
        x=gr.run(lambda x: points.append(x))
        print(f"Termino en {len(points)} pasos")
        print(f"x optima = {x}")
        print(f"f(x)= {get_lambda(self.expr, x.size)(*x)}")
        return points

@dataclass
class GradiantExcerciseClamped(ABC):
    expr: Expr
    x_i: np.ndarray
    minimum: np.ndarray
    maximum: np.ndarray

    def run(self) -> List[np.ndarray]:
        a=0.1
        e1=1e-9
        e2=1e-9
        print(f"X forzado a estar por encima de {self.minimum}")
        print(f"X forzado a estar por debajo de {self.maximum}")

        print(f"Punto inical: {self.x_i}")
        print(f"Razon de aprendizaje: {a}")
        print(f"Precision para dif. de pasos: {e1}")
        print(f"Precision en la pendiente: {e2}")
        gr = GradientDescentClamped(self.x_i, self.expr, a, 1000, e1, e2,self.minimum, self.maximum)
        points = []
        x=gr.run(lambda x: points.append(x))
        print(f"Termino en {len(points)} pasos")
        print(f"x optima = {x}")
        print(f"f(x)= {get_lambda(self.expr, x.size)(*x)}")
        return points


