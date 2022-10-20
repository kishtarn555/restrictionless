from typing import List, Callable
from dataclasses import dataclass

from abc import ABC, abstractmethod

from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import Xn
from optimization.utils.plot import get_colors
from optimization.base.lfo import StepAlgorithm
from optimization.restrictionless.d1.newton import Netwon1D
from optimization.excercises.two.newton1d.base import Excercise
from optimization.excercises.two.secant.base import Excercise as ExSec

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


def f(x):
    return x**2+x**4



@dataclass
class ExcerciseN1(Excercise):

    def plot(self, points:List[float])->None:
        steps=500
        maxi=1e-9
        mini=1e9
        di = (self.x_b-self.x_a)/steps
        for i in range(0, steps+1):
            cx = self.df(self.x_a+di*i)
            if (cx < mini):
                mini=cx
            if (cx > maxi):
                maxi=cx

        mini-=(maxi-mini)*0.1
        X = np.linspace(self.x_a, self.x_b, steps)
        Y = self.df(X)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_title(self.__class__.__name__)
        ax.set_xlim(self.x_a, self.x_b)
        ax.set_ylim(mini, maxi)

        ax.plot(X, Y)
        cols=get_colors(len(points))            
        for i, pt in enumerate(points):
            ax.scatter(
                pt,
                self.df(pt),
                c=cols[i]
            )
            if (i!=0):                
                ax.plot([pt, pt], [self.df(pt),0],c="gray",linestyle='dashed')        
            if (i!= len(points)-1):
                ax.plot([pt, points[i+1]], [self.df(pt),0],c="black")        
        fig.show()


class Task3NewtonFx(Excercise):
    def __init__(self):
        super().__init__(-4.2,2,-4,10,1e-8)
    def f(self, x):
        return f(x)

    def sf(self, x: Expr) -> Expr:
        return self.f(x) # type: ignore


class Task3Newton (ExcerciseN1):
    def __init__(self):
        super().__init__(-4.2,2,-4,10,1e-8)
    def f(self, x):
        return f(x)

    def sf(self, x: Expr) -> Expr:
        return self.f(x) # type: ignore


@dataclass
class SecantModed(ExSec):
    def plot(self, points:List[float])->None:
        steps=500
        maxi=1e-9
        mini=1e9
        sa = self.x_a
        sb = self.x_b
        for pt in points:
            if (sa > pt):
                sa=pt
            if (sb < pt):
                sb=pt
        di = (sb-sa)/steps
        for i in range(0, steps+1):
            cx = self.df(sa+di*i)
            if (cx < mini):
                mini=cx
            if (cx > maxi):
                maxi=cx

        mini-=(maxi-mini)*0.1
        X = np.linspace(sa, sb, steps)
        Y = self.df(X)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_xlim(sa, sb)
        ax.set_ylim(mini, maxi)

        ax.plot(X, Y)
        for i, pt in enumerate(points):
            color = "green"
            if (i <1):
                color = "blue"
            elif (i == len(points)-1):
                color = "red"
            else:
                ax.plot(
                    [pt, pt],
                    [self.df(pt), 0],
                    c="gray",
                    linestyle='dashed'                   
                )
                ax.plot(
                    [pt, points[i+1]],
                    [self.df(pt),0],
                    c="black"                    
                )

                ax.plot(
                    [pt, points[i-1]],
                    [self.df(pt),self.df(points[i-1])],
                    c="gray"                    
                )
            
                    
                
            ax.scatter(pt,self.df(pt), c=color)
        
        fig.show()

class SecantDev(SecantModed):
    def __init__(self):
        super().__init__(-4,-3, 10, 1e-8, 0)
    
    def f(self, x):
        return f(x)

    def sf(self, x: Expr) -> Expr:
        return self.f(x)  # type: ignore


class SecantNorm(ExSec):
    def __init__(self):
        super().__init__(-4,-3, 10, 1e-8, 0)
    
    def f(self, x):
        return f(x)

    def sf(self, x: Expr) -> Expr:
        return self.f(x)  # type: ignore