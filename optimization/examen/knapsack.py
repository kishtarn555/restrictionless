from optimization.utils.lib import *
from collections import deque

from dataclasses import dataclass

import math
import random

from typing import NamedTuple, List

class RunStats(NamedTuple):
    INITIAL_THRESHOLD: float
    T: float
    A : float
    EPS : float
    LR : float
    UR : float


class Item(NamedTuple):
    weight: int
    price: int

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

class solutionData(NamedTuple):
    score: int
    fitness: float
    weight: int



@dataclass(kw_only=True)
class Knapsack:
    TABU_CAPACITY:int

    

    def runKnapsack(self, w:float, items: List[Item]) -> List[int]:
        current_solution = [0] * len(items)
        best_solution = [0] * len(items)
        best = solutionData(0,0,0)

        current = solutionData(0,0,0)


        tabu_list = set()
        tabu_inorder = deque()
        repetitions = max((int)(1e6/len(items)),10)
        for i in range(repetitions):
            # Paso 1, encontrar el mejor vecino
            neighbor = solutionData(0,-1e9, 0)
            changed = -1

            test = current_solution
            for j in range(len(current_solution)):
                if j in tabu_list:
                    continue                
                prev = test[j]
                test[j] = 1 - test[j]
                newScore = current.score + (1 if test[j]==1 else -1)*items[j].price
                newWeight= current.weight + (1 if test[j]==1 else -1)*items[j].weight
                newFitness = newScore if newWeight <= w else (
                    -1e6 - newWeight*1000
                )
                newData = solutionData(newScore,newFitness,newWeight)
                if (newData.fitness > neighbor.fitness):
                    neighbor = newData
                    changed = j                
                test[j]=prev

            if changed == -1:
                print("Fatal error, no best neighbor found")
                exit()

            tabu_list.add(changed)
            tabu_inorder.append(changed)
            if (len(tabu_list) > self.TABU_CAPACITY):
                tabu_list.remove(tabu_inorder[0])
                tabu_inorder.popleft()
            
            current = neighbor
            current_solution[changed] = 1-current_solution[changed]

            if (current.fitness > best.fitness):
                best=current
                best_solution = current_solution.copy()
        print(
            (
                f"> Best Solution got a score of {best.score} " 
                f"with weight {best.weight}, fitness function {best.fitness}"
                )
        )   
             
        return best_solution

def runCase(caseName):
    Knapsack(TABU_CAPACITY=3)
    items: List[Item]


            

        
