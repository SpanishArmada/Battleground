# Hive Class

from GameConstant import GameConstant

class Hive:
    def __init__(self, cPos, rPos, playerID):
        self.cPos = cPos
        self.rPos = rPos
        self.playerID = playerID
        self.hiveTimer = 0

    def getCol(self):
        return self.cPos

    def getRow(self):
        return self.rPos

    def getPlayerID(self):
        return self.playerID

    def getTimer(self):
        return self.hiveTimer

    def setCol(self, cPos):
        self.cPos = cPos

    def setRow(self, rPos):
        self.rPos = rPos

    def setNewPlayer(self, playerID):
        if(self.playerID != playerID):
            self.playerID = playerID
            resetTimer()

    def incrTimer(self):
        self.hiveTimer += 1
        if(self.hiveTimer >= GameConstant.RESPAWN):
            resetTimer()
            return true
        else:
            return false

    def resetTimer(self):
        self.hiveTimer = 0;

