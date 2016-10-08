import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Movement import *
from Unit import *
from HexagridHelper import *
class test1:
    def getAction(self, pid, grids, units, memory): 
        results = []
        counter = 0
        for i in units:
            for j in i:
                if(isinstance(j, int)):
                    continue
                if j.GetUnitID() == pid:
                    if(counter % 3 == 0):
                        results.append(Movement(pid, LEFT))
                    else:
                        results.append(Movement(pid, DOWNLEFT))
                    counter += 1
        return results
        
