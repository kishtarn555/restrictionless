
from optimization.utils.sm.vectorfunc import get_lambda, Xn
from optimization.utils.lib import *
def hessian(f: Expr, xs:arr) -> arr:
    d = xs.size
    return arr(
        [
            [
                get_lambda(sp.diff(sp.diff(f, Xn(i)), Xn(j)),d)(*xs)
                for j in range(d)
            ]
           for i in range(d)
        ]
    )