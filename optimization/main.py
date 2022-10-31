from typing import List, Tuple

from optimization.utils.lib import *
from optimization.meta.hw.backpack import Knapsack, Item, validateSolution, rawWeight, rawScore, RunStats

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
        "ks_19_0":12185,      
        "ks_30_0":99764,      
        "ks_40_0":99924,      
        "ks_45_0":23478,      
        "ks_50_0":140693,      
        "ks_50_1":5277,      
        "ks_60_0":99837,      
        "ks_82_0":104718684,      
        "ks_100_0":99762,      
        "ks_100_1":1327897,      
        "ks_100_2":1000000,      
        "ks_106_0":106922305,      
        "ks_200_0":97829,      
        "ks_200_1":1094384,      
        "ks_300_0":1674996,      
        "ks_400_0":3946489,      
        "ks_500_0":54939,      
        "ks_1000_0":109899,     
        "ks_10000_0":1099893,
    
}

def readCase(path: str) -> Tuple[int, int, List[Item]]:
    f = open(path, "r")
    N, W = map((int), f.readline().split())
    items: List[Item] = []
    for i in range(N):
        p, w = map(float, f.readline().split())
        items.append(Item(w,p))
    return N, W, items



def runCase(name:str, runStats:RunStats, runs:int=1) -> Tuple[float, List[Item]]:
    N, W, items = readCase(f"extern/hw/knap/{name}")
    solver = Knapsack(
        INITIAL_THRESHOLD=runStats.INITIAL_THRESHOLD,
        T=runStats.T,
        A=runStats.A,
        EPS = runStats.EPS,
        LR=runStats.LR,
        UR=runStats.UR
    )
    avgSum =0
    myScore = -1
    solution:List[int] =[]
    scores = []
    for i in range(runs):
        cur = solver.runKnapsack(W, items)
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
    print(f"Got avarage score of {avg}/{optimumDP[name]} = {avg/optimumDP[name]*100.0}")    
    print(f"All scores: {scores}")
    print("--------------------------------------")
    out = open(f"extern/hw/knap/out/{name}.out", "w")
    for pos in solution:
        out.write(f"{pos} ")
    out.write('\n')    
    out.write(f"{rawWeight(items, solution)}\n")
    out.write(f"{rawScore(items, solution)}\n")
        
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
        runCase(
            name,
            default,
            50        
        )

if __name__=="__main__":
    main()