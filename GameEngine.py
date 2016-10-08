# Game Engine

from Grid import Grid
from Unit import Unit
from Hive import Hive
from GameConstant import GameConstant as C
import HexagridHelper as Helper

class GameEngine:

    def __init__(self, col = 50, row = 50, playerNum = 2):
        self.gridTerrainMain = [[C.EMPTY for i in range(col)] for j in range(row)]
        self.gridUnits = [[C.EMPTY for i in range(col)] for j in range(row)]
        self.playerNum = playerNum
        self.row = row
        self.col = col

    def ResetVariables(self):
        # Variables for running AI
        self.gridFoW = [[[C.EMPTY for i in range(self.col)] for j in range(self.row)] for k in range(self.playerNum)]

        # Variables for movement phase
        self.playerMovements = [C.EMPTY for i in range(self.playerNum)]

        # Variables for action phase
        self.gridUnitEnemyScore = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
        self.gridUnitDeathMark = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]

    def Update(self):
        self.ResetVariables()
        self.RunAI()
        self.MovementPhase()
        self.ActionPhase()
        self.WriteToFile()
        pass
        # main function

    def CalculateFoW(self):
        pass
        # generate map for each player
    
    def RunAI(self):
        pass
        # calculate parameters to pass
        # execute ai for each player
        # store movement

    def MovementPhase(self):
        pass
        # check collision
        # place on a new map

    def ActionPhase(self):
        pass
        # Calculate enemy
        # check death
        # apply death

    def CalculateEnemyScore(self):
        for r in range(self.row):
            for c in range(self.col):
                unit = self.gridUnits[r][c]
                if (unit != C.EMPTY):
                    nearbyCoordinates = Helper.GetAllWithinDistance(r,c,C.ATTACK_RANGE)
                    enemyCount = 0
                    for coor in nearbyCoordinates:
                        otherUnit = self.gridUnits[coor[0]][coor[1]]
                        if (otherUnit != C.EMPTY and otherUnit.playerID != unit.playerID):
                            enemyCount+=1
                    self.gridUnitEnemyScore[r][c] = enemyCount

    def CheckDeath(self):
        for r in range(self.row):
            for c in range(self.col):
                unit = self.gridUnits[r][c]
                unitEnemyScore = self.gridUnitEnemyScore[r],[c]
                if (unit != C.EMPTY):
                    nearbyCoordinates = Helper.GetAllWithinDistance(r,c,C.ATTACK_RANGE)
                    minEnemyScore = 100
                    for coor in nearbyCoordinates:
                        otherUnit = self.gridUnits[coor[0]][coor[1]]
                        otherUnitEnemyScore =  self.gridUnitEnemyScore[coor[0]][coor[1]]
                        if (otherUnit != C.EMPTY and otherUnit.playerID != unit.playerID):
                            minEnemyScore = min(minEnemyScore, otherUnitEnemyScore)

                    self.gridUnitDeathMark = minEnemyScore <= unitEnemyScore

    def ApplyDeath(self):
        for r in range(self.row):
            for c in range(self.col):
                pass



    def IsValidCoordinate(self, row, col):
        return (row>=0 and row < self.row and col>=0 and col<self.col)

    def Test(self):
        print(self.gridFoW[0][0][0])

    def WriteToFile(self):
        pass
        # store state for each turn

    