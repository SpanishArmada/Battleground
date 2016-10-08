from GameConstant import GameConstant as C

def addHive(grids, row, col, playerId):
    grids[row][col] = C.PLAYER_HIVE + playerId


def getPercentile(start, end, distance):
    # return point based on how far the distance from start
    # distance is the percentage of distance from (end- start)
    return (start + int((end - start) * distance))

def addType1(grids, rowStart, rowEnd, colStart, colEnd):
    """
    100001 <-- rowStart
    100001
    100001
    100001 <-- rowEnd
    """
    for i in range(rowStart, rowEnd + 1):
        grids[i][colStart] = grids[i][colEnd] = C.WALL 


def addType2(grids, rowStart, rowEnd, colStart, colEnd):
    """
    11111
    00000
    00000
    11111
    """
    for i in range (colStart, colEnd + 1):
        grids[rowStart][i] = grids[rowEnd][i] = C.WALL

def addType3(grids, rowStart, rowEnd, colStart, colEnd, interval):
    """
    10001
    00000 --> interval = 1
    10001
    00000
    10001
    """
    for i in range(rowStart, rowEnd + 1):
        if(i % (interval + 1) == 0):
            grids[i][colStart] = grids[i][colEnd] = C.WALL

def addType4(grids, row, col, size):
    """
    10000 for each corner
    11000
    11100
    11110
    11111
    """
    counter = 1
    for i in range(row - size, row):
        temp = counter
        for j in range(0, size):
            if(temp > 0):
                grids[i][j] = C.WALL
                temp -= 1
            else:
                grids[i][j] = C.NON_WALL
        counter += 1
    counter = 5
    for i in range(0, size):
        temp = counter
        for j in range(0, size):
            if(temp > 0):
                grids[i][j] = C.WALL
                temp -= 1
            else:
                grids[i][j] = C.NON_WALL
        counter -= 1
    counter = 5
    for i in range(0, size):
        temp = counter
        for j in range(col - 1, col - size - 1, -1):
            if(temp > 0):
                grids[i][j] = C.WALL
                temp -= 1
            else:
                grids[i][j] = C.NON_WALL
        counter -= 1
    counter = 1
    for i in range(row - size, row):
        temp = counter
        for j in range(col - 1, col - size - 1, -1):
            if(temp > 0):
                grids[i][j] = C.WALL
                temp -= 1
            else:
                grids[i][j] = C.NON_WALL
        counter += 1

def addRiver(grids, rowStart, rowEnd, colStart, colEnd, bridge):
    """
    11111
    11111
    00000 --> bridge = 2
    00000
    11111
    11111
    """
    for i in range(rowStart, rowStart + (rowEnd - rowStart + 1 - bridge) / 2):
        for j in range(colStart, colEnd + 1):
            grids[i][j] = C.WALL
    for i in range(rowStart + rowStart + (rowEnd - rowStart + 1 - bridge) / 2  + bridge, rowEnd + 1):
        for j in range(colStart, colEnd + 1):
            grids[i][j] = C.WALL

def getMap(row, col):
    grids = [[C.NON_WALL for i in range(row)] for j in range(col)]
    addHive(grids, getPercentile(0, row, 0.5), 2, 0)    #player 0
    addHive(grids, getPercentile(0, row, 0.5), col - 3) #player 1
    addHive(grids, 5, 10, -1)                           #not taken
    addHive(grids, row - 5, 10, -1)                     #not taken
    addHive(grids, 5, col - 10, -1)                     #not taken
    addHive(grids, row - 5, col - 10, -1)               #not taken
    addType4(grids, row, col, 5)
    addRiver(grids, 0, row - 1, getPercentile(0, col, 0.5) - 2, getPercentile(0, col, 0.5) + 2, 5)
    addType3(grids, 0, 7, 7, 12, 1)
    addType3(grids, row - 8, row - 2, col - 14, col - 8, 1)
    addType1(grids, getPercentile(0, row, 0.7), getPercentile(0, row, 0.85), getPercentile(0, col, 0.2), getPercentile(0, col, 0.35))
    addType1(grids, getPercentile(0, row, 0.15), getPercentile(0, row, 0.3), getPercentile(0, col, 0.65), getPercentile(0, col, 0.8))
    addType2(grids, getPercentile(0, row, 0.3), getPercentile(0, row, 0.4), getPercentile(0, col, 0.8), getPercentile(0, col, 0.9))
    addType2(grids, getPercentile(0, row, 0.6), getPercentile(0, row, 0.7), getPercentile(0, col, 0.1), getPercentile(0, col, 0.2))
    return grids
