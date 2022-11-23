from optimization.utils.lib import *
from collections import deque

from dataclasses import dataclass

import math
import random

from typing import NamedTuple, List, Tuple

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

    def shouldPrint(self, index:int, len:int) -> bool:
        if (index == 0): 
            return True        
        if ((index-1)//(len//100) !=(index)//(len//100) ):
            return True
        return False


    def runKnapsack(self, w:float, items: List[Item]) -> Tuple[List[int],List[Tuple[int, int, int]]]:
        # Paso 0, iniciamos con una solucion vacia, con el vector 0
        steps = []
        current_solution = [0] * len(items)
        best_solution = [0] * len(items)
        best = solutionData(0,0,0)

        current = solutionData(0,0,0)


        tabu_list = set()
        tabu_inorder = deque()
        repetitions = max((int)(1e6/len(items)),10)
        steps.append((0, 0, 0))
        for i in range(repetitions):
            # Paso 1, encontrar el mejor vecino
            neighbor = solutionData(0,-1e9, 0)
            changed = -1
            test = current_solution
            # Iteramos por todos los vecinos
            for j in range(len(current_solution)):
                # Si este vecino viola la lista tabu, lo ignoramos
                if j in tabu_list:
                    continue                
                prev = test[j]
                test[j] = 1 - test[j]
                # Calculamos los valores para este vecino
                newScore = current.score + (1 if test[j]==1 else -1)*items[j].price
                newWeight= current.weight + (1 if test[j]==1 else -1)*items[j].weight
                newFitness = newScore if newWeight <= w else (
                    - newWeight
                )
                newData = solutionData(newScore,newFitness,newWeight)
                #Vemos si este vecino es el mejor vecino encontrado
                if (newData.fitness > neighbor.fitness):
                    neighbor = newData
                    changed = j                
                test[j]=prev

            if changed == -1:
                print("Fatal error, no best neighbor found")
                print(f"Knapsack {len(tabu_list)}")
                sum=0
                for x in current_solution:
                    sum+=x
                print(f"With {sum} elements")
                print(f"With {current.weight} weight")
                exit()
            

            # Paso 2 Cambiar la solucion actual por el vecino
            current = neighbor
            current_solution[changed] = 1-current_solution[changed]
            sh = self.shouldPrint(i, repetitions) or i < 20
            
            # Paso 3 agregar el cambio a la lista tabu
            tabu_list.add(changed)
            tabu_inorder.append(changed)
            if (len(tabu_list) > self.TABU_CAPACITY):
                tabu_list.remove(tabu_inorder[0])
                tabu_inorder.popleft()

            # Paso 4 Comparar la solucion actual con la mejor, y de ser necesario actualizarla
            if (current.fitness > best.fitness):
                best=current
                best_solution = current_solution.copy()
                sh = True

            if (sh):                
                steps.append((i+1, best.score, current.score))
        
        steps.append((repetitions, best.score, current.score))    

        print(
            (
                f"> Best Solution got a score of {best.score} " 
                f"with weight {best.weight}, using |T| = {self.TABU_CAPACITY}"
                )
        )   
             
        return (best_solution,steps)

def runCase(caseName):
    Knapsack(TABU_CAPACITY=3)
    items: List[Item]


            

        
