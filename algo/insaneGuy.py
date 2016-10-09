import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Movement import *
from Unit import *
from HexagridHelper import *
import random

class insaneGuy:
    def getAction(self, pid, grids, units, memory):
        self.grids = grids
        maxrow = len(units)
        maxcol = len(units[0])
        self.isOccupied = [[False for i in range(maxcol)] for j in range(maxrow)]
        results = []
        counter = 0
        for i in range(maxcol-1,-1,-1):
            for j in range(maxrow):
                if (isinstance(units[j][i], int)):
                    continue
                if units[j][i].GetPlayerID() == pid:
                    results.append(Movement(units[j][i].GetUnitID(), random.randint(1,6)))
        return results

    def isValidMove(self,coor):
        if (self.grids[coor[0]][coor[1]] == 1):
            return False
        return not self.isOccupied[coor[0]][coor[1]]
