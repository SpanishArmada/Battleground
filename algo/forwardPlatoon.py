import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Movement import *
from Unit import *
from HexagridHelper import *

class forwardPlatoon:
    def getAction(self, pid, grids, units, memory):
        self.pid = pid
        self.grids = grids
        self.units = units
        self.maxrow = len(units)
        self.centerRow = self.maxrow//2
        self.maxcol = len(units[0])
        self.isOccupied = [[False for i in range(self.maxcol)] for j in range(self.maxrow)]
        results = []
        counter = 0
        for i in range(self.maxcol):
            for j in range(self.maxrow):
                if (isinstance(units[j][i], int)):
                    continue
                if units[j][i].GetPlayerID() == pid:
                    if (self.isOccupied[j][i] or grids[j][i]>=9):
                        movrig = GetMoveTarget(j,i,RIGHT)
                        movuprig = GetMoveTarget(j,i,UPPERRIGHT)
                        movdowrig = GetMoveTarget(j,i,DOWNRIGHT)
                        if (j < self.centerRow): #above middle
                            if (self.isValidMove(movdowrig)):
                                results.append(Movement(units[j][i].GetUnitID(), DOWNRIGHT))
                                self.isOccupied[movdowrig[0]][movdowrig[1]] = True
                            elif (self.isValidMove(movrig)):
                                results.append(Movement(units[j][i].GetUnitID(), RIGHT))
                                self.isOccupied[movrig[0]][movrig[1]] = True
                            elif (self.isValidMove(movuprig)):
                                results.append(Movement(units[j][i].GetUnitID(), UPPERRIGHT))
                                self.isOccupied[movuprig[0]][movuprig[1]] = True
                            else:
                                results.append(Movement(units[j][i].GetUnitID(), IDLE))
                                self.isOccupied[j][i] = True

                        elif (j > self.centerRow): #below middle
                            if (self.isValidMove(movuprig)):
                                results.append(Movement(units[j][i].GetUnitID(), UPPERRIGHT))
                                self.isOccupied[movuprig[0]][movuprig[1]] = True
                            elif (self.isValidMove(movrig)):
                                results.append(Movement(units[j][i].GetUnitID(), RIGHT))
                                self.isOccupied[movrig[0]][movrig[1]] = True
                            elif (self.isValidMove(movdowrig)):
                                results.append(Movement(units[j][i].GetUnitID(), DOWNRIGHT))
                                self.isOccupied[movdowrig[0]][movdowrig[1]] = True
                            else:
                                results.append(Movement(units[j][i].GetUnitID(), IDLE))
                                self.isOccupied[j][i] = True

                        else: # center
                            if (self.isValidMove(movrig)):
                                results.append(Movement(units[j][i].GetUnitID(), RIGHT))
                                self.isOccupied[movrig[0]][movrig[1]] = True
                            elif (self.isValidMove(movuprig)):
                                results.append(Movement(units[j][i].GetUnitID(), UPPERRIGHT))
                                self.isOccupied[movuprig[0]][movuprig[1]] = True
                            elif (self.isValidMove(movdowrig)):
                                results.append(Movement(units[j][i].GetUnitID(), DOWNRIGHT))
                                self.isOccupied[movdowrig[0]][movdowrig[1]] = True
                            else:
                                results.append(Movement(units[j][i].GetUnitID(), IDLE))
                                self.isOccupied[j][i] = True
        return results

    def isValidMove(self,coor):
        if (coor[0]<0 or coor[0]>=self.maxrow or coor[1]<0 or coor[1]>=self.maxcol):
            return False
        if (self.grids[coor[0]][coor[1]] == 1):
            return False
        if (not isinstance(self.units[coor[0]][coor[1]], int)):
            if (self.units[coor[0]][coor[1]].GetPlayerID() == self.pid):
                return False
        return not self.isOccupied[coor[0]][coor[1]]
