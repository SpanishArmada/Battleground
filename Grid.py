# Grid class

from GameConstant import GameConstant

class Grid:
    def __init__(self, gridType, hive = GameConstant.EMPTY):
        self.gridType = gridType
        self.hive = hive
    
    def GetType(self):
        return self.gridType

    def GetHive(self):
        return self.hive

    def SetType(self, gridType, hive = GameConstant.EMPTY):
        self.gridType = gridType
        self.hive = hive

    def SetHype(self, hive = GameConstant.EMPTY):
        self.hive = hive