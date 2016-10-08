import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Movement import *
from Unit import *
from HexagridHelper import *
class test:
    def getAction(self, pid, grids, units, memory): 
        results = []
        counter = 0
        for i in units:
            for j in i:
                if(isinstance(j, int)):
                    continue
                if j.GetPlayerID() == pid:
                    if(counter % 2 == 0):
                        results.append(Movement(j.GetUnitID(), RIGHT))
                    else:
                        results.append(Movement(j.GetUnitID(), UPPERRIGHT))
                    counter += 1
        return results
