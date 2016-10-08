# Unit class

class Unit:
    def __init__(self, unitID, playerID):
        self.unitID = unitID
        self.playerID = playerID

    def GetUnitID(self):
        return self.unitID

    def GetPlayerID(self):
        return self.playerID

    def SetUnitID(Self, unitID):
        self.unitID = unitID

    def SetPlayerID(self, playerID):
        self.playerID = playerID