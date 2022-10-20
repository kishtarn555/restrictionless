from optimization.exam2.a1 import Task1
from optimization.exam2.a2 import Task2
# from optimization.exam2.a3 import (
#     Task3Newton,
#     Task3NewtonFx,
#     SecantDev,
#     SecantNorm
# )
from optimization.exam2.a4 import (
    Task3Newton,
    Task3NewtonFx,
    SecantDev,
    SecantNorm
)
from optimization.exam2.a5 import (
    Ej5NewtonUnidimensionl1 as Ej5NU1,
    Ej5NewtonUnidimensionl2 as Ej5NU2,
    Ej5SecX1,
    Ej5SecX2,
    Ej5Newton2D,
    f as f5
)

from optimization.exam2.a6 import Ej6Newton

from optimization.exam2.a7 import Ej7Newton

def task3or4():
    Task3NewtonFx().run()
    x = Task3Newton().run()

    print()
    

    SecantDev().run()
    SecantNorm().run()

def task5():
    print("Newton unidimensional para x1:")
    x1 = Ej5NU1().run()
    print()
    
    print("Newton unidimensional para x2:")
    x2 = Ej5NU2().run()
    print("Juntando los newtons unidimensionales obtenemos:")
    print(f"x=({x1},{x2})")
    print(f"f({x1},{x2})={f5(x1,x2)}")

    print()
    print("Secante para x_1")
    x1 = Ej5SecX1().run()    
    print("Secante para x_2")
    x2 = Ej5SecX2().run()    
    print("Juntando las dos secantes obtenemos:")
    print(f"x=({x1},{x2})")
    print(f"f({x1},{x2})={f5(x1,x2)}")

    print()
    print("Usando Newton en dos dimensiones")
    x= Ej5Newton2D().run()
    print(f"x1 = {x[0]}")
    print(f"x2 = {x[1]}")
    print(f"f({x[0]},{x[1]}) = {f5(x[0], x[1])}")

def task6():
    x = Ej6Newton().run()
    print(f"x=({x[0]}, {x[1]})")
    print(f"f({x[0]}, {x[1]}) = {Ej6Newton().fk(*x)}")

def task7():
    ej = Ej7Newton()
    x = ej.run()
    print(f"x=({x[0]}, {x[1]}, {x[2]}, {x[3]})")

    print(f"f(x)= {ej.fk(*x)}")

if __name__ == "__main__":
    task3or4()
    input("Press a key to end...")