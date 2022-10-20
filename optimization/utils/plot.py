from typing import List
def get_colors(size:int) -> List[str]:
    res=[]
    for i in range(size):
        if i == 0:
            res.append("blue")
        elif i == size-1:
            res.append("red")
        else:
            res.append("green")
    return res