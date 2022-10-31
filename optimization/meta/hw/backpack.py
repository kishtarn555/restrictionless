from  optimization.utils.lib import *
from dataclasses import dataclass

import math
import random

from typing import NamedTuple, List\

class RunStats(NamedTuple):
    INITIAL_THRESHOLD: float
    T: float
    A : float
    EPS : float
    LR : float
    UR : float


class Item(NamedTuple):
    weight: float
    price: float

def rawScore( items: List[Item], selection:List[int]) -> float:
    score: float = 0
    for i, item in enumerate(items):
        if (selection[i] == 1):
            score += item.price
    return score


def rawWeight( items: List[Item], selection:List[int]) -> float:
    weight: float = 0
    for i, item in enumerate(items):
        if (selection[i] == 1):
            weight += item.weight
    return weight


def validateSolution(w: float, items: List[Item], selection:List[int]) -> float:
    if (len (selection)!= len(items)):
        return -1e9
    score: float = rawScore(items, selection)
    weight: float = rawWeight(items, selection)
    if (weight > w):
        score = -1e9
    return score


@dataclass(kw_only=True)
class Knapsack:
    INITIAL_THRESHOLD: float
    T: float
    A : float
    EPS : float
    LR : float
    UR : float

    def mutate (self, x: List[int], items: List[Item]) -> List[int]:
        sp: int = math.ceil(len(x)* (random.random()*(self.UR-self.LR)+self.LR) )
        response = x.copy()
        for tmp in range(sp):
            i = random.randint(0, len(x)-1)
            response[i] = 1-response[i]
        return response 

    def runKnapsack(self, w:float, items: List[Item]) -> List[int]:
        threshold = self.INITIAL_THRESHOLD
        x = [1 for tmp in items]
        t = self.T
        scoreX = validateSolution(w, items, x)
        while scoreX < 0:
            x = [
                1 
                if np.random.random() < threshold 
                else 0 
                for tmp in items
            ]
            scoreX = validateSolution(w, items, x)
            threshold*=0.99
            
        while t > self.EPS:
            xt = self.mutate(x, items)
            newScore = validateSolution(w, items, xt)
            if (newScore > scoreX):
                scoreX = newScore
                x = xt.copy()
            elif (np.random.random() < np.exp(-(scoreX-newScore)/t)):            
                scoreX = newScore
                x = xt.copy()
            t*=self.A
        return x
            

        
