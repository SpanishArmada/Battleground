# Grid class

from GameConstant import GameConstant

class Grid:
    def __init__(self, gridType, hive = GameConstant.EMPTY):
        self.gridType = gridType
        self.hive = hive
    
    def getType(self):
        return self.gridType

    def getHive(self):
        return self.hive

    def setType(self, gridType, hive = GameConstant.EMPTY):
        self.gridType = gridType
        self.hive = hive

    def setHype(self, hive = GameConstant.EMPTY:
        self.hive = hive