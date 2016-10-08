# Unit class

class Unit:
    def __init__(self, unitID, playerID, rPos, cPos):
        self.unitID = unitID
        self.playerID = playerID
        self.rPos = rPos
        self.cPos = cPos

    def GetRow(self):
        return self.rPos

    def GetUnitID(self):
        return self.unitID

    def GetPlayerID(self):
        return self.playerID

    def GetCol(self):
        return self.cPos

    def SetUnitID(Self, unitID):
        self.unitID = unitID

    def SetPlayerID(self, playerID):
        self.playerID = playerID

    def SetRow(self, rPos):
        self.rPos = rPos

    def SetCol(self, cPos):
        self.cPos = cPos