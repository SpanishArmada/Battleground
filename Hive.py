# Hive Class

from GameConstant import GameConstant

class Hive:
    def __init__(self, rPos, cPos, playerID):
        self.cPos = cPos
        self.rPos = rPos
        self.playerID = playerID
        self.hiveTimer = 0

    def GetCol(self):
        return self.cPos

    def GetRow(self):
        return self.rPos

    def GetPlayerID(self):
        return self.playerID

    def GetTimer(self):
        return self.hiveTimer

    def SetCol(self, cPos):
        self.cPos = cPos

    def SetRow(self, rPos):
        self.rPos = rPos

    def SetNewPlayer(self, playerID):
        if(self.playerID != playerID):
            self.playerID = playerID
            self.ResetTimer()

    def IncrTimer(self, freeOnTop):
        self.hiveTimer += 1
        if(self.hiveTimer >= GameConstant.RESPAWN and freeOnTop):
            self.ResetTimer()
            return True
        else:
            return False

    def ResetTimer(self):
        self.hiveTimer = 0;

