from typing import List
from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import Xn
from optimization.excercises.two.newton1d.base import Excercise as ExcNew1D
from optimization.excercises.two.secant.base import Excercise as ExcSec
from optimization.restrictionless.newton import Newton

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

class Ej6Newton:
    def __init__(self):        
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')    
        self.x_i = arr([9,8])
        self.lx=0
        self.ly=0
        self.lz=-5
        self.rx=10
        self.ry=10
        self.rz=1200
    
    def fk(self,x1,x2):
        return (x1+2*x2-7)**2 + (2*x1+x2-5)**1.5
        
    def step(self, x, pts:List[np.ndarray]):
        print(f"x_{len(pts)} : {x}")
        pts.append(x)
        
    def run(self):
        exp = self.fk(Xn(0), Xn(1)) 
        newt = Newton(self.x_i, 1e-9, 1e-9, 1, exp)
        
        points =[newt.x_i]
        
        print(f"x_{0} : {newt.x_i}")
        x = newt.run(lambda x: self.step(x, points))
        print (f"Termino en {len(points)-1} pasos:")
        self.scale([
            [self.lx,self.rx],
            [self.ly,self.ry],
            [self.lz,self.rz],
            ])
        self.plotf(points)
        return x


    
    def scale(self,dimensions: List[List[int]]):    
        self.ax.set_aspect('equal') 
        self.ax.set_xlim(np.array(dimensions[0])) # type: ignore
        self.ax.set_ylim(np.array(dimensions[1])) # type: ignore
        self.ax.set_zlim(np.array(dimensions[2])) # type: ignore
    

    def plotf(self, points):
        x = np.linspace(self.lx, self.rx, 30)
        y = np.linspace(self.ly, self.ry, 30)
        X, Y = np.meshgrid(x, y)
        Z = self.fk(X, Y)
        self.ax.plot_wireframe(X, Y, Z, color='gray')         # type: ignore
        self.fig.show()
        zdata = np.array([self.fk(*pt) for pt in points])
        xdata =  np.array([pt[0] for pt in points])
        ydata = np.array([pt[1] for pt in points])
        for i, pt in enumerate(points):
            xd = pt[0]
            yd = pt[1]
            zd = self.fk(*pt)
            if i == 0:
                self.ax.scatter(xd, yd, zd,  facecolor="blue")
            elif i == len(points)-1:
                self.ax.scatter(xd, yd, zd,  facecolor="red")
            else:
                self.ax.scatter(xd, yd, zd,  facecolor="green")

   