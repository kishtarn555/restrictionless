from typing import List
from abc import abstractmethod
from dataclasses import dataclass

from optimization.utils.lib import *

from optimization.utils.sm.vectorfunc import get_lambda
from optimization.excercises.two.gradiant.base import GradiantExcercise
import matplotlib.pyplot as plt

@dataclass
class Excercise2D (GradiantExcercise):
    lx:int
    rx:int
    ly:int
    ry:int
    lz:int
    rz:int

    def scale(self,dimensions: List[List[int]]):    
        self.ax.set_aspect('equal') 
        
        self.ax.set_xlim(np.array(dimensions[0])) # type: ignore magic
        self.ax.set_ylim(np.array(dimensions[1])) # type: ignore magic
        self.ax.set_zlim(np.array(dimensions[2])) # type: ignore magic
    
    @abstractmethod
    def fk(self,x,y):
        pass


    def plotf(self):
        x = np.linspace(self.lx, self.rx, 30)
        y = np.linspace(self.ly, self.ry, 30)
        X, Y = np.meshgrid(x, y)
        Z = self.fk(X, Y)
        self.ax.plot_wireframe(X, Y, Z, color='gray')  # type: ignore     
        self.fig.show()
        
    def run(self)->None:
        points = super().run()
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        self.scale([
            [self.lx,self.rx],
            [self.ly,self.ry],
            [self.lz,self.rz],
        ])
        self.plotf()
        zdata = np.array(
            [get_lambda(self.expr,self.x_i.size)(*pt) for pt in points]
        )
        xdata =  np.array([pt[0] for pt in points])
        ydata = np.array([pt[1] for pt in points])
        self.ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens_r')   # type: ignore
        self.ax.set_title(self.__class__.__name__)
        self.fig.show()
        