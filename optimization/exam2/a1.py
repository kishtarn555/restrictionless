from typing import List
from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import Xn
from optimization.restrictionless.newton import Newton

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

class Task1:

    def __init__(self):        
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')    
        self.x_i = arr([1,1])
        self.lx=-2
        self.ly=-2
        self.lz=-2
        self.rx=1
        self.ry=1
        self.rz=5
    
    def fk(self,x1,x2):
        return (x1**2*np.e**x1+x2**2*np.e**x2+1
        )
    def step(self, x, pts:List[np.ndarray]):
        print(f"x_{len(pts)} : {x}")
        pts.append(x)
        
    def run(self):
        exp = self.fk(Xn(0), Xn(1)) 
        newt = Newton(self.x_i, 1e-9, 1e-9, 1, exp)
        
        points =[newt.x_i]
        
        print(f"x_{0} : {newt.x_i}")
        x = newt.run(lambda x: self.step(x, points))
        print (f"Finished on {len(points)-1} steps:")
        print(f"x={x}")
        print(f"f({x})={self.fk(*x)}")
        self.scale([
            [self.lx,self.rx],
            [self.ly,self.ry],
            [self.lz,self.rz],
            ])
        self.plotf(points)


    
    def scale(self,dimensions: List[List[int]]):    
        self.ax.set_aspect('equal') 
        self.ax.set_xlim(np.array(dimensions[0]))
        self.ax.set_ylim(np.array(dimensions[1]))
        self.ax.set_zlim(np.array(dimensions[2]))
    

    def plotf(self, points):
        x = np.linspace(self.lx, self.rx, 30)
        y = np.linspace(self.ly, self.ry, 30)
        X, Y = np.meshgrid(x, y)
        Z = self.fk(X, Y)
        self.ax.plot_wireframe(X, Y, Z, color='gray')        
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

    def f(self, x):
        return 3*x**4+(x-1)**2

    def sf(self, x):
        return self.f(x)