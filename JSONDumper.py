import json


# JSON Format:
#   root: dictionary of map and turn data
#       map: 2D([row][col]) list of integer
#       turn data: list (index = turn no) of turn details
#           turn details: dict(), consists of unitData, baseData and deadData
#               unitData: list of unit details
#                   unitDetails: [row, col, owner ID]
#               baseData: list of hive details
#                   hiveDetails: [row, col, owner ID] (-1 for no owner)
#               deadData: list of dead details, positions where units died in this turn
#                   deadDetails: [row, col, owner ID] (100 for multiple owners' units death)
#   example:
#   {
#       map: [[0,0,0,0][0,1,1,0][9,0,0,9]]
#       turnData:
#           [
#               {
#                   unitData: [[0,0,1], [2,2,5], [4,0,0]]
#                   baseData: [[5,5,0], [10,5,1], [9,9,-1]]
#               },
#               {
#                   unitData: [[0,1,1], [2,3,5], [4,1,0]]
#                   baseData: [[5,5,0], [10,5,1], [9,9,-1]]
#               },
#           ]
#   }

class JSONDumper:
    def __init__(self):
        self.data = dict()

    def InitializeMap(self, terrainMap):
        self.data["map"] = terrainMap
        self.turnData = []

    def Update(self, unitDictionary, hiveList, gridDeathPos):
        newUnitList = []
        for key in unitDictionary.keys():
            pid = unitDictionary[key].GetPlayerID()
            row = unitDictionary[key].GetRow()
            col = unitDictionary[key].GetCol()
            newUnitList.append([row,col,pid])

        newHiveList = []
        for hive in hiveList:
            pid = hive.GetPlayerID()
            row = hive.GetRow()
            col = hive.GetCol()
            newHiveList.append([row,col,pid])

        newDeadList = []
        for r in range(len(gridDeathPos)):
            for c in range(len(gridDeathPos[r])):
                if (gridDeathPos[r][c] != -1):
                    pid = gridDeathPos[r][c]
                    newDeadList.append([r, c, pid])

        newTurnData = dict()
        newTurnData["unitData"] = newUnitList
        newTurnData["baseData"] = newHiveList
        newTurnData["deadData"] = newDeadList
        self.turnData.append(newTurnData)

    def GetDump(self):
        self.data["turnData"] = self.turnData
        return json.dumps(self.data)