from GameConstant import GameConstant as C

def addHive(grids, row, col, playerId, fort):
    grids[row][col] = C.PLAYER_HIVE + playerId
    if(fort):
        addFort(grids, row, col, 1, [1, 1, 1, 1])
        

def addFort(grids, row, col, gateSize, opening):
    top  = row - 3
    bot = row + 3
    left = col - 3
    right = col + 3
    for i in range(left, right + 1):
        grids[top][i] = C.WALL
        grids[bot][i] = C.WALL
    for i in range(top, bot + 1):
        grids[i][right] = C.WALL
        grids[i][left] = C.WALL
    # opening = (opening - 1) / 2
    # direction = [[top, col], [row, right], [bot, col], [row, left]]
    # for i in 
    grids[top][col] = grids[bot][col] = C.NON_WALL
    grids[row][right] = grids[row][left] = C.NON_WALL

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

def addPlus(grids, row, col, size):
    """
    size = 2
    001100
    001100 
    111111
    111111
    001100
    001100
    """
    part = size // 3
    iCounter = 0
    for i in range(row, row + size):
        jCounter = 0
        for j in range(col, col + size):
            r = iCounter // part
            c = jCounter // part
            jCounter += 1
            if((r + c) % 2 == 0 and not (r == 1 and c == 1)):
                grids[i][j] = C.NON_WALL
            else:
                grids[i][j] = C.WALL
        iCounter += 1

def getMap(row, col):
    grids = [[C.NON_WALL for i in range(row)] for j in range(col)]
    addHive(grids, getPercentile(0, row, 0.4), 10, 0, True)    #player 0
    addHive(grids, getPercentile(0, row, 0.5), col - 3, 1, False) #player 1
    addHive(grids, 5, 10, -1, False)                           #not taken
    addHive(grids, row - 5, 10, -1, False)                     #not taken
    addHive(grids, 5, col - 10, -1, False)                     #not taken
    addHive(grids, row - 5, col - 10, -1, False)               #not taken
    addType4(grids, row, col, 5)
    addRiver(grids, 0, row - 1, getPercentile(0, col, 0.5) - 2, getPercentile(0, col, 0.5) + 2, 5)
    addType3(grids, 0, getPercentile(0, row, 0.15), getPercentile(0, col, 0.15), getPercentile(0, col, 0.25), 1)
    addType3(grids, getPercentile(0, row, 0.85), row - 2, getPercentile(0, col, 0.75), getPercentile(0, col, 0.85), 1)
    addType1(grids, getPercentile(0, row, 0.7), getPercentile(0, row, 0.85), getPercentile(0, col, 0.2), getPercentile(0, col, 0.35))
    addType1(grids, getPercentile(0, row, 0.15), getPercentile(0, row, 0.3), getPercentile(0, col, 0.65), getPercentile(0, col, 0.8))
    addType2(grids, getPercentile(0, row, 0.3), getPercentile(0, row, 0.4), getPercentile(0, col, 0.8), getPercentile(0, col, 0.9))
    addType2(grids, getPercentile(0, row, 0.6), getPercentile(0, row, 0.7), getPercentile(0, col, 0.1), getPercentile(0, col, 0.2))
    return grids

def getMap2(row, col):
    grids = [[C.NON_WALL for i in range(row)] for j in range(col)]
    addHive(grids, getPercentile(0, row, 0.5), 2, 0, False)    #player 0
    addHive(grids, getPercentile(0, row, 0.5), col - 3, 1, False) #player 1
    addHive(grids, getPercentile(0, row, 0.2), getPercentile(0, col, 0.2), -1, False)  #not taken
    addHive(grids, getPercentile(0, row, 0.8), getPercentile(0, col, 0.8), -1, False)  #not taken
    addHive(grids, getPercentile(0, row, 0.2), getPercentile(0, col, 0.8), -1, False)  #not taken
    addHive(grids, getPercentile(0, row, 0.8), getPercentile(0, col, 0.2), -1, False)  #not taken
    # addType4(grids, row, col, 5)
    addPlus(grids, 4, 4, 9)
    addPlus(grids, 4, col - 13, 9)
    addPlus(grids, row - 13, 4, 9)
    addPlus(grids, row - 13, col - 13, 9)
    addFort(grids, getPercentile(0, row, 0.5), getPercentile(0, col, 0.5), 1, [1, 1, 1, 1])
    return grids


def getMap3(row,col):
    grids = [[C.NON_WALL for i in range(col)] for j in range(row)]
    middleRow = (row//2)

    addHive(grids, middleRow,   2,            0, False)  #player 0
    addHive(grids, middleRow,   col - 2 - 1,  1, False)  #player 1
    addHive(grids, 2,           5,           -1, False)  #not taken
    addHive(grids, row - 2 - 1, 5,           -1, False)  #not taken
    addHive(grids, 2,           col - 5 - 1, -1, False)  #not taken
    addHive(grids, row - 2 - 1, col - 5 - 1, -1, False)  #not taken
    # addType4(grids, row, col, 5)
    return grids
