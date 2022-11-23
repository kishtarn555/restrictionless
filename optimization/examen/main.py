from typing import List, Tuple
import math
from optimization.utils.lib import *
from optimization.examen.knapsack import Knapsack, Item, validateSolution, rawWeight, rawScore, RunStats

names = [
    "ks_4_0",       
    "ks_19_0",      
    "ks_30_0",      
    "ks_40_0",      
    "ks_45_0",      
    "ks_50_0",      
    "ks_50_1",      
    "ks_60_0",      
    "ks_82_0",      
    "ks_100_0",      
    "ks_100_1",      
    "ks_100_2",      
    "ks_106_0",      
    "ks_200_0",      
    "ks_200_1",      
    "ks_300_0",      
    "ks_400_0",      
    "ks_500_0",      
    "ks_1000_0",     
    "ks_10000_0",
]

optimumDP = {
    
        "ks_4_0":19,       
        "ks_19_0":12248,      
        "ks_30_0":99798,      
        "ks_40_0":99924,      
        "ks_45_0":23974,      
        "ks_50_0":142156,      
        "ks_50_1":5345,      
        "ks_60_0":99837,      
        "ks_82_0":104723596,      
        "ks_100_0":99837,      
        "ks_100_1":1333930,      
        "ks_100_2":10892,      
        "ks_106_0":106925262,      
        "ks_200_0":100236,      
        "ks_200_1":1103604,      
        "ks_300_0":1688692,      
        "ks_400_0":3967180,      
        "ks_500_0":54939,      
        "ks_1000_0":109899,     
        "ks_10000_0":1099893,
    
}

def readCase(path: str) -> Tuple[int, int, List[Item]]:
    f = open("../"+path, "r")
    N, W = map((int), f.readline().split())
    items: List[Item] = []
    for i in range(N):
        p, w = map(int, f.readline().split())
        items.append(Item(w,p))
    return N, W, items



def runCase(name:str, runStats:RunStats, runs:int=1) -> Tuple[float, List[Item]]:
    N, W, items = readCase(f"extern/hw/knap/{name}")
    solver = Knapsack(
        TABU_CAPACITY= (int)(math.log2(N))
    )
    avgSum =0
    myScore = -1
    solution:List[int] =[]
    scores = []
    steps = []
    for i in range(runs):
        cur, msteps = solver.runKnapsack(W, items)
        steps=msteps.copy()
        curScore = validateSolution(W, items, cur)
        avgSum +=curScore
        scores.append(curScore)
        if (curScore > myScore ):
            myScore= curScore
            solution= cur.copy()

    avg = avgSum/runs
    myScore = validateSolution(W, items, solution)

    print(f"For {name} got best score: {myScore}/{optimumDP[name]}= {myScore/optimumDP[name]*100.0}")
    print(f"Using items: {[i+1 for i,p in enumerate(solution) if p==1 ]}")
    print(f"Got average score of {avg}/{optimumDP[name]} = {avg/optimumDP[name]*100.0}")    
    print(f"All scores: {scores}")
    print("--------------------------------------")
    out = open(f"../extern/hw/knap/out/{name}.out", "w")
    for pos in solution:
        out.write(f"{pos} ")
    out.write('\n')    
    out.write(f"{rawWeight(items, solution)}\n")
    out.write(f"{rawScore(items, solution)}\n")

    csv = open(f"../extern/hw/knap/csv/{name}.csv", "w")
    csv.write("i,s_i,w_i\n")
    for it in steps:
        csv.write(f"{it[0]},{it[1]},{it[2]}\n")
        
    return (
        myScore,
        [
            items[i] 
            for i, included in enumerate(solution)
            if included == 1
        ]
    )



def main():
    print()
    print()
    default = RunStats(
            INITIAL_THRESHOLD=1,
            T=1000,
            A=0.995,
            EPS=1e-6,
            LR=0.05,
            UR=0.1
    )
    
    for name in names:
        print(f"Running case {name}")
        runCase(
            name,
            default,
            1        
        )

if __name__=="__main__":
    main()