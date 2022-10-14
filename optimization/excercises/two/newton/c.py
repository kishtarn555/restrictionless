from typing import List

from optimization.restrictionless.newtonclamp import NewtonClamped
from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import get_lambda
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


class ExcC:
    def scale(self,dimensions: List[List[int]]):    
        self.ax.set_aspect('equal') 
        self.ax.set_xlim(np.array(dimensions[0]))
        self.ax.set_ylim(np.array(dimensions[1]))
        self.ax.set_zlim(np.array(dimensions[2]))
    
    def fk(self,x1,x2):
        return 0.1*( 12+ x1**2 + (1+x1**2)/(x1**2)+(100+x1**2 * x2**2)/(x1*x2)**4 )

    def plotf(self):
        x = np.linspace(0.5, 10, 30)
        y = np.linspace(0.5, 10, 30)
        X, Y = np.meshgrid(x, y)
        Z = self.fk(X, Y)
        self.ax.plot_wireframe(X, Y, Z, color='gray')        
        self.fig.show()
        
    def main(self)->None:
        e=parse_expr("0.1*( 12+ x1**2 + (1+x1**2)/(x1**2)+(100+x1**2 * x2**2)/(x1*x2)**4   )")
        print(e)
        ntw =  NewtonClamped(np.array([9.0,2.0]), 1e-9, 1e-9,0.05, e, arr([0,0]), arr([10,10]))
        points =[]
        x= ntw.run( lambda x: points.append(np.copy(x)))
        print (f"Finished on {len(points)} steps:")
        print(f"x={x}")
        print(f"f({x})={get_lambda(e, x.size)(*x)}")
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')    
        self.scale([
            [0,10],
            [0,10],
            [-10, 10],
            ])
        # Data for three-dimensional scattered points
        zdata = np.array([get_lambda(e,x.size)(*pt) for pt in points])
        xdata =  np.array([pt[0] for pt in points])
        ydata = np.array([pt[1] for pt in points])
        self.ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens_r')
        self.plotf()
        