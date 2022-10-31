from typing import NamedTuple, List
from optimization.utils.lib import *


class Item(NamedTuple):
    weight: float
    score: float

def mutate(x: List[int], mutation:float) -> List[int]:    
    return [ (i if np.random.random()> mutation else 1-i) for i in x]

def validate(x:List[int],w, data:List[Item]):
    ws = 0
    score=0
    for ind, itm in enumerate(data):
        if x[ind]==1:
            ws += itm.weight
            score += itm.score
    if ws < w:
        score -=1e6
    return score


def run(w: float, data:List[Item], T:float, a:float):    
    x: List[int] = [ (1 if np.random.random()>0.5 else 0) for i in data]
    curscore= validate(x, w, data)
    while (T > 1e-6):
        xs = mutate(x, 0.05)
        nexts = validate(xs, w, data)
        if ( curscore< nexts ):
            x=xs
            curscore=nexts
        elif np.random.random() < np.exp((curscore-nexts)/T):            
            x=xs
            curscore=nexts
        T = T * a
    print(curscore)
    print(x)
    


