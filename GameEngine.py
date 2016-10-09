# Game Engine

from Unit import Unit
from Hive import Hive
from Movement import Movement
from GameConstant import GameConstant as C
from JSONDumper import JSONDumper
import HexagridHelper as Helper
import copy as copy
from os.path import isfile, join, dirname, splitext, abspath, split
import imp, importlib
import sys
import traceback
class GameEngine:

    # Init function
    def __init__(self, row = 50, col = 50, playerNum = 2):
        self.row = row
        self.col = col
        self.playerNum = playerNum
        self.gridTerrainMain = [[C.EMPTY for i in range(col)] for j in range(row)]
        self.gridUnits = [[C.EMPTY for i in range(col)] for j in range(row)]
        self.unitDictionary = dict()
        self.unitCount = 0
        self.hiveList = []
        self.memoryList = [{} for i in range(playerNum)]
        self.turnNumber = 0
        self.hiveScore = [0 for i in range(playerNum)]
        self.unitScore = [0 for i in range(playerNum)]

        self.jsonDumper = JSONDumper()

    # Resets variables for an update cycle
    def ResetVariables(self):
        self.gridFoW = [[[C.EMPTY for i in range(self.col)] for j in range(self.row)] for k in range(self.playerNum)]
        self.playerMovements = [C.EMPTY for i in range(self.playerNum)]
        self.gridUnitEnemyScore = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
        self.gridUnitDeathMark = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
        self.gridDeathPositions = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
        self.turnHiveScore = [0 for i in range(self.playerNum)]
        self.turnUnitScore = [0 for i in range(self.playerNum)]

    # Clears gridUnits and recalculates it based on unitDictionary
    # To be called whenever a unitDictionary is modified (a unit is moved/killed)
    def ResetGridUnits(self):
        self.gridUnits = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]
        for key, unit in self.unitDictionary.items():
            self.gridUnits[unit.GetRow()][unit.GetCol()] = unit


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
        print("Selected", playerObject[0], playerObject[1])
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
        pid = self.OnePlayerLeft()
        if (self.OnePlayerLeft() != C.EMPTY):
            self.jsonDumper.SetWinner(pid, C.WINCON_WIPEOUT);
            return True
        elif(self.TurnExceeded()):
            self.CheckWinner()
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
                return C.EMPTY

        for key, unit in self.unitDictionary.items():
            curID = unit.GetPlayerID()
            if(curID != playerLeft and curID != C.EMPTY):
                return C.EMPTY

        return playerLeft

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

    # Calculates each player's fog of war
    def CalculateFoW(self):
        # generate map for each player
        for key, tmpUnit in self.unitDictionary.items():
            if(tmpUnit != C.EMPTY):
                listViewed = Helper.GetAllWithinDistance(tmpUnit.GetRow(), tmpUnit.GetCol(), C.VISION_RANGE)
                for coor in listViewed:
                    if(self.IsValidCoordinate(coor[0],coor[1])):
                        self.gridFoW[tmpUnit.GetPlayerID()][coor[0]][coor[1]] = C.REVEALED
        
        for hive in self.hiveList:
            if(hive.GetPlayerID() != C.EMPTY):
                listViewed = Helper.GetAllWithinDistance(hive.GetRow(), hive.GetCol(), C.VISION_RANGE)
                for coor in listViewed:
                    if(self.IsValidCoordinate(coor[0],coor[1])):
                        self.gridFoW[hive.GetPlayerID()][coor[0]][coor[1]] = C.REVEALED

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
            try:
                self.playerMovements[i] = self.playerObject[i].getAction(i, gridTerrainPlayer[i], gridUnitsPlayer[i], self.memoryList[i])
            except:
                print ("Exception in user code: Player ", i)
                print ('-'*60)
                traceback.print_exc(file=sys.stdout)
                print ('-'*60)
                self.playerMovements[i] = []
                for key, unit in self.unitDictionary.items():
                    if(key == i):
                        self.playerMovements[i].append(Movement(unit.GetUnitID(),Helper.IDLE))

    # Movement phase, handles all the outputs of players' scripts and moves units concurrently
    # Any collision will cause all units in the tile to die
    def MovementPhase(self):
        isMovedUnit = {}
        isDeathMatrix = [[C.EMPTY for i in range(self.col)] for j in range(self.row)]

        for i in range(self.playerNum):
            for mov in self.playerMovements[i]:
                if(mov.GetUnitID() in self.unitDictionary.keys() and not(mov.GetUnitID() in isMovedUnit.keys()) ):
                    curUnit = self.unitDictionary[mov.GetUnitID()]
                    oRow = curUnit.GetRow()
                    oCol = curUnit.GetCol()
                    if(curUnit.GetPlayerID() == i):
                        nCoor = Helper.GetMoveTarget(oRow, oCol, mov.GetMove())
                        if(self.IsValidCoordinate(nCoor[0], nCoor[1]) and self.gridTerrainMain[nCoor[0]][nCoor[1]] != C.WALL):
                            curUnit.SetRow(nCoor[0])
                            curUnit.SetCol(nCoor[1])
                    isMovedUnit[mov.GetUnitID()] = True
        
        # check collision

        deathList = []
        for key, curUnit in self.unitDictionary.items():
            if(isDeathMatrix[curUnit.GetRow()][curUnit.GetCol()] == C.EMPTY):
                isDeathMatrix[curUnit.GetRow()][curUnit.GetCol()] = curUnit.GetUnitID()
            else:
                deathList.append(curUnit.GetUnitID())
                deathList.append(isDeathMatrix[curUnit.GetRow()][curUnit.GetCol()])

        for deathTarget in deathList:
            self.KillUnit(deathTarget)
        
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
                if (self.IsValidCoordinate(coor[0], coor[1])):
                    otherUnit = self.gridUnits[coor[0]][coor[1]]
                    if (otherUnit != C.EMPTY and otherUnit.GetPlayerID() != unit.GetPlayerID()):
                        # print(r,c,unit.GetPlayerID(),"VS",coor[0],coor[1],otherUnit.GetPlayerID())
                        enemyCount+=1
            self.gridUnitEnemyScore[r][c] = enemyCount

    # If a unit has enemies near him, check the enemy score of those enemies as well
    # If the enemy score of this unit is >= the minimum of all enemies' score, mark this unit for death
    def CheckDeath(self):
        for key, unit in self.unitDictionary.items():
            r = unit.GetRow()
            c = unit.GetCol()
            unitEnemyScore = self.gridUnitEnemyScore[r][c]
            # print ("unit of player", unit.GetPlayerID(),"at",r,c,"Score=",unitEnemyScore)
            if (unitEnemyScore == 0):
                continue
            nearbyCoordinates = Helper.GetAllWithinDistance(r,c,C.ATTACK_RANGE)
            minEnemyScore = 100
            for coor in nearbyCoordinates:
                if (self.IsValidCoordinate(coor[0], coor[1])):
                    otherUnit = self.gridUnits[coor[0]][coor[1]]
                    otherUnitEnemyScore =  self.gridUnitEnemyScore[coor[0]][coor[1]]
                    if (otherUnit != C.EMPTY and otherUnit.GetPlayerID() != unit.GetPlayerID()):
                        minEnemyScore = min(minEnemyScore, otherUnitEnemyScore)

            if (minEnemyScore <= unitEnemyScore):
                self.gridUnitDeathMark[r][c] = 1

    # Apply all death marks to units
    def ApplyDeath(self):

        deathIDUnit = []

        for key, unit in self.unitDictionary.items():
            r = unit.GetRow()
            c = unit.GetCol()
            if (self.gridUnitDeathMark[r][c] == 1):
                deathIDUnit.append(unit.GetUnitID())

        for id in deathIDUnit:
            self.KillUnit(id)

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
        # print("Kill unitID", unitId)
        killedUnit = self.unitDictionary.pop(unitId, None)
        if (killedUnit != None):
            playerOwner = killedUnit.GetPlayerID()
            if (self.gridDeathPositions[killedUnit.GetRow()][killedUnit.GetCol()] == -1):
                self.gridDeathPositions[killedUnit.GetRow()][killedUnit.GetCol()] = playerOwner
            else:
                self.gridDeathPositions[killedUnit.GetRow()][killedUnit.GetCol()] = 100 # Multiple players' units died here
        return killedUnit!=None

    # Checks if this coordinate is valid
    def IsValidCoordinate(self, row, col):
        return (row>=0 and row < self.row and col>=0 and col<self.col)
    
    # Spawn unit in every hive if timer end and no unit on top
    def UpdateArena(self):
        # update timer for each hives
        for hive in self.hiveList:
            unitOnTop = self.gridUnits[hive.GetRow()][hive.GetCol()]

            if(unitOnTop != C.EMPTY):
                if(unitOnTop.GetPlayerID() != hive.GetPlayerID()):
                    hive.SetNewPlayer(unitOnTop.GetPlayerID())
                    self.gridTerrainMain[hive.GetRow()][hive.GetCol()] = C.PLAYER_HIVE + hive.GetPlayerID()
                    continue
                else:
                    freeOnTop = False
            else:
                freeOnTop = True

            if(hive.GetPlayerID() != C.EMPTY):
                if(hive.IncrTimer(freeOnTop)):
                    self.AddUnit(hive.GetPlayerID(), hive.GetRow(), hive.GetCol())



    # Updates the JSON every turn with the turn's arena status
    def UpdateJSON(self):
        self.CountPlayerScore()
        self.jsonDumper.Update(self.unitDictionary, self.hiveList, self.gridDeathPositions, self.turnHiveScore, self.turnUnitScore)
        # store state for each turn

    # Update counter of players' no. of hives and units
    def CountPlayerScore(self):
        for hive in self.hiveList:
            if (hive.GetPlayerID() != C.EMPTY):
                self.turnHiveScore[hive.GetPlayerID()] += 1

        for key,unit in self.unitDictionary.items():
            if (unit.GetPlayerID() != C.EMPTY):
                self.turnUnitScore[unit.GetPlayerID()] += 1

        for i in range(self.playerNum):
            self.hiveScore[i] += self.turnHiveScore[i]
            self.unitScore[i] += self.turnUnitScore[i]

    # In case of turn limit, find winner based on score
    # Check hive score first, if tie check unit score, if still tied then return tie.
    def CheckWinner(self):
        maxscore = 0
        winnerId = -1
        tie = False
        for i in range(len(self.hiveScore)):
            if (self.hiveScore[i] > maxscore):
                maxscore = self.hiveScore[i]
                winnerId = i
                tie = False
            elif (self.hiveScore[i] == maxscore):
                tie = True

        if (not tie):
            self.jsonDumper.SetWinner(winnerId, C.WINCON_HIVESCORE)
            return

        maxscore = 0
        winnerId = -1
        tie = False
        for i in range(len(self.unitScore)):
            if (self.unitScore[i] > maxscore):
                maxscore = self.unitScore[i]
                winnerId = i
                tie = False
            elif (self.unitScore[i] == maxscore):
                tie = True

        if (not tie):
            self.jsonDumper.SetWinner(winnerId, C.WINCON_UNITSCORE)
            return

        self.jsonDumper.SetWinner(-1, C.WINCON_TIE)