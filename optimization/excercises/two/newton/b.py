from typing import List

from optimization.restrictionless.newton import Newton
from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import get_lambda, Xn
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


class ExcB:
    def scale(self,dimensions: List[List[int]]):    
        self.ax.set_aspect('equal') 
        self.ax.set_xlim(np.array(dimensions[0]))
        self.ax.set_ylim(np.array(dimensions[1]))
        self.ax.set_zlim(np.array(dimensions[2]))
    
    def fk(self,x,y):
        return 4*x**2-4*x*y+3*y**2+x

    def plotf(self):
        x = np.linspace(-5, 5, 30)
        y = np.linspace(-5, 5, 30)
        X, Y = np.meshgrid(x, y)
        Z = self.fk(X, Y)
        self.ax.plot_wireframe(X, Y, Z, color='gray')        
        self.fig.show()
        
    def main(self)->None:
        e=4*Xn(0)**2-4*Xn(0)*Xn(1)+3*Xn(1)**2+Xn(0)
        print(e)
        ntw =  Newton(np.array([4.0,4.0]), 1e-9, 1e-9,0.5, e)
        points =[arr([4,4])]
        x= ntw.run( lambda x: points.append(np.copy(x)))
        print (f"Finished on {len(points)} steps:")
        print(f"x={x}")
        print(f"f({x})={get_lambda(e, x.size)(*x)}")
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')    
        self.scale([
            [-5,5],
            [-5,5],
            [0, 200],
            ])
        # Data for three-dimensional scattered points
        zdata = np.array([get_lambda(e,x.size)(*pt) for pt in points])
        xdata =  np.array([pt[0] for pt in points])
        ydata = np.array([pt[1] for pt in points])
        self.ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens_r')
        self.plotf()
        