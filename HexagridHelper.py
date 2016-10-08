# Battleground uses the 'odd-r' horizontal layout convention for its hexagonal grid.
# For more information, check www.redblobgames.com/grids/hexagons/#coordinates
#
# [0,0] [0,1] [0,2] [0,3] [0,4]
#    [1,0] [1,1] [1,2] [1,3] [1,4]
# [2,0] [2,1] [2,2] [2,3] [2,4]
#    [3,0] [3,1] [3,2] [3,3] [3,4]
# [4,0] [4,1] [4,2] [4,3] [4,4]

# Movement naming Convention
#  [UL] [UR]
# [L] [I] [R]
#  [DL] [DR]
# I = 0, R..UR = 1..6 in clockwise order

import GameConstant

DCOL_ODDROW  = [0, 1, 1, 0, -1, 0, 1]
DCOL_EVENROW = [0, 1, 0, -1, -1, -1, 0]
DROW = [0, 0, 1, 1, 0, -1, -1]

# Simulates a 1-step movement in [direction] direction from the source coordinate
# Returns a tuple containing the target coordinate (row,col)
def GetMoveTarget(sourceRow, sourceCol, direction):
    if (sourceRow%2 == 1): # For odd rows
        return sourceRow + DROW[direction], sourceCol + DCOL_ODDROW[direction]
    else: # For even rows
        return sourceRow + DROW[direction], sourceCol + DCOL_EVENROW[direction]

# Collects all coordinates within [distance] distance from the source coordinate
# Returns a list of tuples containing the possible coordinates (row,col)
def GetAllWithinDistance(sourceRow, sourceCol, distance):
    coorList=[(sourceRow,sourceCol)]
    for i in range(distance):
        newList = []
        for coor in coorList:
            for dir in range(0,7):
                newList.append(GetDirectionTarget(coor[0],coor[1],dir))
        coorList = list(set(newList))
    return coorList

# Returns the step distance between two coordinates
def GetDistance(aRow, aCol, bRow, bCol):
    rowDist = abs(aRow - bRow)
    colDist = abs(aCol - bCol)
    bIsLeftFromA = (bCol < aCol)

    steps = 0
    if (rowDist % 2 == 1):
        steps += 1
        rowDist -= 1
        if ((aRow % 2 == 0 and bIsLeftFromA) or (aRow % 2 == 1 and not(bIsLeftFromA))):
            colDist -= 1

    steps += rowDist
    colDist -= rowDist//2

    if (colDist > 0):
        steps += colDist

    return steps




