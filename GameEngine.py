# Game Engine

from Grid import Grid
from Unit import Unit
from Hive import Hive
from GameConstant import GameConstant as C
import HexagridHelper

class GameEngine:

    def __init__(self, col = 50, row = 50, playerNum = 2):
        self.gridTerrainMain = [[C.EMPTY for i in range(col)] for j in range(row)]
        self.gridUnits = [[C.EMPTY for i in range(col)] for j in range(row)]
        self.gridFoW = [[[C.EMPTY for i in range(col)] for j in range(row)] for k in range(playerNum)]
        self.playerMovements = [C.EMPTY for i in range(playerNum)]
        self.playerNum = playerNum
        self.row = row
        self.col = col
         

    def Update(self):
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
                pass

    def IsValidCoordinate(self, row, col):
        return (row>=0 and row < self.row and col>=0 and col<self.col)

    def writeToFile(self):
        pass
        # store state for each turn

    