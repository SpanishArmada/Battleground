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
        self.unitDictionary = dict()
        self.memoryList = [0 for i in range(playerNum)]
        self.playerNum = playerNum
        self.row = row
        self.col = col
        self.unitCount = 0

    def ResetGridUnits(self):
        self.gridUnits = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
        for key, unit in self.unitDictionary.items():
            self.gridUnits[unit.GetRow][unit.GetCol] = unit

    def ResetVariables(self):
        # Variables for running AI
        self.gridFoW = [[[C.EMPTY for i in range(self.col)] for j in range(self.row)] for k in range(self.playerNum)]

        # Variables for movement phase
        self.playerMovements = [C.EMPTY for i in range(self.playerNum)]

        # Variables for action phase
        self.gridUnitEnemyScore = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
        self.gridUnitDeathMark = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
    
    def Start(gridTerrainMain, playerObject):
        self.playerObject = playerObject

    def Update(self):
        self.ResetVariables()
        self.RunAI()
        self.MovementPhase()
        self.ActionPhase()
        self.WriteToFile()
        pass
        # main function

    def CalculateFoW(self):
        # generate map for each player
        for i in range(self.row):
            for j in range(self.col):
                tmpUnit = self.gridUnits[i][j]
                if(tmpUnit != C.EMPTY):
                    listViewed = Helper.GetAllWithinDistance(i, j, C.VISION_RANGE)
                    for coor in listViewed:
                        if(IsValidCoordinate(coor[0],coor[1])):
                            self.gridFoW[tmpUnit.GetPlayerID()][coor[0]][coor[1]] = C.REVEALED
    
    def RunAI(self):
        # calculate parameters to pass
        gridUnitsPlayer = [[[C.EMPTY for i in range(self.col)] for j in range(self.row)] k in range(self.playerNum)]
        gridTerraiMain = [[[C.EMPTY for i in range(self.col)] for j in range(self.row)] k in range(self.playerNum)]

        for i in range(self.playerNum):
            for j in range(self.row):
                for k in range(self.col):
                    if(self.gridFoW[i][j][k] == 1)
        # execute ai for each player
        # store movement

    def MovementPhase(self):
        isDeathMatrix = [[0 for i in range(self.col)] in range(self.row)]

        for i in range(self.playerNum):
            for mov in self.playerMovements[i]:
                if(self.unitDictionary.has_key(mov.getUnitID)):
                    curUnit = self.unitDictionary[mov.getUnitID()]
                    oRow = curUnit.GetRow()
                    oCol = curUnit.GetCol()
                    if(curUnit.GetPlayerID() == i):
                        nCoor = Helper.GetMoveTarget(oRow, oCol, mov.getMove())
                        if(IsValidCoordinate(nCoor[0], nCoor[1]) and self.gridTerrainMain[nCoor[0]][nCoor[1]] != C.WALL):
                            curUnit.SetRow(nCoor[0])
                            curUnit.SetCol(nCoor[1])
        
        # check collision
        for curUnit in self.unitDictionary:
            if(isDeathMatrix[curUnit.GetRow][curUnit.GetCol] == 0):
                isDeathMatrix[curUnit.GetRow][curUnit.GetCol] == curUnit.getUnitID()
            else:
                KillUnit(curUnit.getUnitID())
                KillUnit(isDeathMatrix[curUnit.GetRow][curUnit.GetCol])
        
        # place on a new map
        resetGridUnits() 

    def ActionPhase(self):
        self.CalculateEnemyScore()
        self.CheckDeath()
        self.ApplyDeath()

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

                    self.gridUnitDeathMark[r][c] = minEnemyScore <= unitEnemyScore

    def ApplyDeath(self):
        for r in range(self.row):
            for c in range(self.col):
                unit = self.gridUnits[r][c]
                if (unit != C.EMPTY and self.gridUnitDeathMark[r][c]):
                    self.KillUnit(unit.GetUnitID)
        self.ResetGridUnits()


    def AddUnit(self, playerId, row, col):
        newUnitId = self.unitCount # TODO: make a hash function for id
        newUnit = Unit(newUnitId, playerId, row, col)
        self.unitDictionary[newUnitId] = newUnit
        self.gridUnits[row][col] = newUnit
        self.unitCount += 1
        pass

    def KillUnit(self, unitId):
        killedUnit = self.unitDictionary.pop(unitId, None)
        return killedUnit!=None

    def IsValidCoordinate(self, row, col):
        return (row>=0 and row < self.row and col>=0 and col<self.col)

    def Test(self):
        print(self.gridFoW[0][0][0])

    def WriteToFile(self):
        pass
        # store state for each turn

    