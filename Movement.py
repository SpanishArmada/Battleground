# Movement class

class Movement:
    def __init__(self, unitID, moveDirection):
        self.unitID = unitID
        self.moveDirection = moveDirection

    def GetUnitID(self):
        return self.unitID

    def GetMove(self):
        return self.moveDirection

    def SetUnitID(Self, unitID):
        self.unitID = unitID

    def SetMove(self, moveDirection):
        self.moveDirection = moveDirection