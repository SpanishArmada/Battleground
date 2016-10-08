# Game Engine

from Unit import Unit
from Hive import Hive
from GameConstant import GameConstant as C
from JSONDumper import JSONDumper
import HexagridHelper as Helper
import copy as copy
from os.path import isfile, join, dirname, splitext, abspath, split
import imp, importlib
class GameEngine:

    # Init function
    def __init__(self, col = 50, row = 50, playerNum = 2):
        self.row = row
        self.col = col
        self.playerNum = playerNum

        self.gridTerrainMain = [[C.EMPTY for i in range(col)] for j in range(row)]
        self.gridUnits = [[C.EMPTY for i in range(col)] for j in range(row)]

        self.unitDictionary = dict()
        self.unitCount = 0
        self.hiveList = []
        self.memoryList = [0 for i in range(playerNum)]
        self.turnNumber = 0

        self.jsonDumper = JSONDumper()


    def LoadFromFile(self, filepath, expectedClass):
        class_inst = None

        mod_name,file_ext = splitext(split(filepath)[-1])

        if file_ext.lower() == '.py':
            py_mod = imp.load_source(mod_name, filepath)

        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)

        if hasattr(py_mod, expectedClass):
            class_inst = getattr(py_mod, expectedClass)()

        return class_inst

    # Function to be called. Simulates the game and returns the json dump
    def Start(self, gridTerrain, playerObject):
        path = dirname(abspath(__file__)) + '\\' + "algo" + '\\'
        playerObject[0] = self.LoadFromFile(path + playerObject[0], playerObject[0][:-3])
        playerObject[1] = self.LoadFromFile(path + playerObject[1], playerObject[1][:-3])
        self.ReadTerrain(gridTerrain)
        self.jsonDumper.InitializeMap(gridTerrain)
        self.playerObject = playerObject
        while not self.GameHasEnded():
            self.Update()
        return self.jsonDumper.GetDump()

    # Copies input terrain and stores the hives into hiveList
    def ReadTerrain(self, gridTerrain):
        for i in range(self.row):
            for j in range(self.col):
                self.gridTerrainMain[i][j] = gridTerrain[i][j]
                if (gridTerrain[i][j] >= C.EMPTY_HIVE): # Hive
                    newHive = Hive(i,j,gridTerrain[i][j]-C.PLAYER_HIVE)
                    self.hiveList.append(newHive)

    # True if ending condition for the game has been fulfilled
    # Either a) Turn limit reached, or b) all hives+units belong to one player
    def GameHasEnded(self):
        if(self.TurnExceeded()):
            return True
        elif(self.OnePlayerLeft()):
            return True
        else:
            return False
    
    # check if turn limit exceeded
    def TurnExceeded(self):
        return (self.turnNumber > C.TURN_LIMIT)

    # check if only one player left
    def OnePlayerLeft(self):
        playerLeft = C.EMPTY

        for hive in self.hiveList:
            curID = hive.GetPlayerID()
            if(playerLeft == C.EMPTY):
                playerLeft = curID
                continue

            if(curID != playerLeft and curID != C.EMPTY):
                return False

        for key, unit in self.unitDictionary.items():
            curID = unit.GetPlayerID()
            if(curID != playerLeft and curID != C.EMPTY):
                return False

        return True   

    # Main function to be called per turn.
    # Performs everything in order.
    def Update(self):
        self.ResetVariables()
        self.RunAI()
        self.MovementPhase()
        self.ActionPhase()
        self.UpdateArena()
        self.UpdateJSON()
        self.turnNumber += 1

    # Resets variables for an update cycle
    def ResetVariables(self):
        self.gridFoW = [[[C.EMPTY for i in range(self.col)] for j in range(self.row)] for k in range(self.playerNum)]
        self.playerMovements = [C.EMPTY for i in range(self.playerNum)]
        self.gridUnitEnemyScore = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
        self.gridUnitDeathMark = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]

    # Clears gridUnits and recalculates it based on unitDictionary
    # To be called whenever a unitDictionary is modified (a unit is moved/killed)
    def ResetGridUnits(self):
        self.gridUnits = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
        for key, unit in self.unitDictionary.items():
            self.gridUnits[unit.GetRow()][unit.GetCol()] = unit

    # Calculates each player's fog of war
    def CalculateFoW(self):
        # generate map for each player
        for i in range(self.row):
            for j in range(self.col):
                tmpUnit = self.gridUnits[i][j]
                if(tmpUnit != C.EMPTY):
                    listViewed = Helper.GetAllWithinDistance(i, j, C.VISION_RANGE)
                    for coor in listViewed:
                        if(self.IsValidCoordinate(coor[0],coor[1])):
                            self.gridFoW[tmpUnit.GetPlayerID()][coor[0]][coor[1]] = C.REVEALED

    # Runs each player's AI function
    def RunAI(self):
        self.CalculateFoW()
        gridUnitsPlayer = [[[C.EMPTY for i in range(self.col)] for j in range(self.row)] for k in range(self.playerNum)]
        gridTerrainPlayer = [[[C.EMPTY for i in range(self.col)] for j in range(self.row)] for k in range(self.playerNum)]
        
        # Calculate parameters to pass
        for i in range(self.playerNum):
            for j in range(self.row):
                for k in range(self.col):
                    if(self.gridFoW[i][j][k] == C.REVEALED):
                        gridUnitsPlayer[i][j][k] = copy.deepcopy(self.gridUnits[j][k])
                        gridTerrainPlayer[i][j][k] = copy.deepcopy(self.gridTerrainMain[j][k])

        # execute ai for each player
        # store player movement
        for i in range(self.playerNum):
            self.playerMovements[i] = self.playerObject[i].getAction(i, gridTerrainPlayer[i], gridUnitsPlayer[i], self.memoryList[i])

    # Movement phase, handles all the outputs of players' scripts and moves units concurrently
    # Any collision will cause all units in the tile to die
    def MovementPhase(self):
        isDeathMatrix = [[0 for i in range(self.col)] for j in range(self.row)]

        for i in range(self.playerNum):
            for mov in self.playerMovements[i]:
                if(mov.GetUnitID() in self.unitDictionary.keys()):
                    curUnit = self.unitDictionary[mov.GetUnitID()]
                    oRow = curUnit.GetRow()
                    oCol = curUnit.GetCol()
                    if(curUnit.GetPlayerID() == i):
                        nCoor = Helper.GetMoveTarget(oRow, oCol, mov.GetMove())
                        if(self.IsValidCoordinate(nCoor[0], nCoor[1]) and self.gridTerrainMain[nCoor[0]][nCoor[1]] != C.WALL):
                            curUnit.SetRow(nCoor[0])
                            curUnit.SetCol(nCoor[1])
        
        # check collision
        for key, curUnit in self.unitDictionary.items():
            if(isDeathMatrix[curUnit.GetRow()][curUnit.GetCol()] == 0):
                isDeathMatrix[curUnit.GetRow()][curUnit.GetCol()] == curUnit.GetUnitID()
            else:
                self.KillUnit(curUnit.GetUnitID())
                self.KillUnit(isDeathMatrix[curUnit.GetRow()][curUnit.GetCol()])
        
        # place on a new map
        self.ResetGridUnits()

    # Action phase, handles all the automatic battling of near units
    def ActionPhase(self):
        self.CalculateEnemyScore()
        self.CheckDeath()
        self.ApplyDeath()

    # First calculates the enemy score of units - no of enemies within attack range of an unit
    def CalculateEnemyScore(self):
        for key, unit in self.unitDictionary.items():
            r = unit.GetRow()
            c = unit.GetCol()
            nearbyCoordinates = Helper.GetAllWithinDistance(r,c,C.ATTACK_RANGE)
            enemyCount = 0
            for coor in nearbyCoordinates:
                otherUnit = self.gridUnits[coor[0]][coor[1]]
                if (otherUnit != C.EMPTY and otherUnit.GetPlayerID() != unit.GetPlayerID()):
                    print(r,c,unit.GetPlayerID(),"VS",coor[0],coor[1],otherUnit.GetPlayerID())
                    enemyCount+=1
            self.gridUnitEnemyScore[r][c] = enemyCount

    # If a unit has enemies near him, check the enemy score of those enemies as well
    # If the enemy score of this unit is >= the minimum of all enemies' score, mark this unit for death
    def CheckDeath(self):
        for key, unit in self.unitDictionary.items():
            r = unit.GetRow()
            c = unit.GetCol()
            unitEnemyScore = self.gridUnitEnemyScore[r][c]
            print ("unit of player", unit.GetPlayerID(),"at",r,c,"Score=",unitEnemyScore)
            if (unitEnemyScore == 0):
                continue
            nearbyCoordinates = Helper.GetAllWithinDistance(r,c,C.ATTACK_RANGE)
            minEnemyScore = 100
            for coor in nearbyCoordinates:
                otherUnit = self.gridUnits[coor[0]][coor[1]]
                otherUnitEnemyScore =  self.gridUnitEnemyScore[coor[0]][coor[1]]
                if (otherUnit != C.EMPTY and otherUnit.GetPlayerID() != unit.GetPlayerID()):
                    minEnemyScore = min(minEnemyScore, otherUnitEnemyScore)

            if (minEnemyScore <= unitEnemyScore):
                self.gridUnitDeathMark[r][c] = 1

    # Apply all death marks to units
    def ApplyDeath(self):
        for key, unit in self.unitDictionary.items():
            r = unit.GetRow()
            c = unit.GetCol()
            if (self.gridUnitDeathMark[r][c] == 1):
                self.KillUnit(unit.GetUnitID())
        self.ResetGridUnits()

    # Adds a new unit owned by playerId, at [row, col] to unitDictionary
    # Also automatically gives it a unique ID, and increments the unit counter
    def AddUnit(self, playerId, row, col):
        newUnitId = self.unitCount # TODO: make a hash function for id
        newUnit = Unit(newUnitId, playerId, row, col)
        self.unitDictionary[newUnitId] = newUnit
        self.gridUnits[row][col] = newUnit
        self.unitCount += 1

    # Deletes a unit with ID unitId from unitDictionary.
    # NOTE: Run ResetGridUnits after killing any unit to update the grid!
    def KillUnit(self, unitId):
        print("Kill unitID", unitId)
        killedUnit = self.unitDictionary.pop(unitId, None)
        return killedUnit!=None

    # Checks if this coordinate is valid
    def IsValidCoordinate(self, row, col):
        return (row>=0 and row < self.row and col>=0 and col<self.col)
    
    # Spawn unit in every hive if timer end and no unit on top
    def UpdateArena(self):
        # update timer for each hives
        for hive in self.hiveList:
            if(hive.GetPlayerID() != C.EMPTY):
                unitOnTop = self.gridUnits[hive.GetRow()][hive.GetCol()]

                if(unitOnTop != C.EMPTY):
                    if(unitOnTop.GetPlayerID() != hive.GetPlayerID()):
                        hive.SetNewPlayer(unitOnTop.GetPlayerID())
                        continue
                    else:
                        freeOnTop = False
                else:
                    freeOnTop = True
                
                if(hive.IncrTimer(freeOnTop)):
                    self.AddUnit(hive.GetPlayerID(), hive.GetRow(), hive.GetCol())


    # Updates the JSON every turn with the turn's arena status
    def UpdateJSON(self):
        self.jsonDumper.Update(self.unitDictionary, self.hiveList)
        # store state for each turn
