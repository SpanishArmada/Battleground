import json

class JSONDumper:

    # JSON Format:
    # root: dictionary of init + turn data
    # {
    #   map : 2D list of integer
    #   int : dictionary of data per turn
    #       {
    #           unitData : list of unit details
    #               [
    #                   [row, col, owner player ID]
    #               ]
    #           baseData : list of hive details
    #               [
    #                   [row, col, owner player ID] - -1 for no owner
    #               ]
    #       }
    # }

    def __init__(self):
        self.data = dict()

    def InitializeMap(self, terrainMap):
        self.data["map"] = terrainMap

    def Update(self, iterationID, unitDictionary, hiveList):
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

        turnData = dict()
        turnData["unitData"] = newUnitList
        turnData["baseData"] = newHiveList
        self.data[iterationID] = turnData

    def GetDump(self):
        return json.dumps(self.data)