from GameConstant import GameConstant as C
def addHive(grids, row, col):
    grids[row][col] = C.HIVE


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
    111111111
    111101111
    111000111
    110000011
    100000001
    000000000
    100000001
    110000011
    111000111
    111101111
    111111111
    """
    counter = 0
    # for i in range (row, row + size):
    #     for i in ra

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
    addHive(grids, getPercentile(0, row, 0.5), 0)
    addHive(grids, getPercentile(0, row, 0.5), col - 1)
    addRiver(grids, 0, row - 1, getPercentile(0, col, 0.5) - 2, getPercentile(0, col, 0.5) + 2, 5)
    addType3(grids, 0, 7, 7, 12, 1)
    addType3(grids, row - 7, row - 1, col - 7, col - 1, 1)
    addType1(grids, getPercentile(0, row, 0.7), getPercentile(0, row, 0.85), getPercentile(0, col, 0.2), getPercentile(0, col, 0.35))
    addType1(grids, getPercentile(0, row, 0.15), getPercentile(0, row, 0.3), getPercentile(0, col, 0.65), getPercentile(0, col, 0.8))
    addType2(grids, getPercentile(0, row, 0.3), getPercentile(0, row, 0.4), getPercentile(0, col, 0.8), getPercentile(0, col, 0.9))
    addType2(grids, getPercentile(0, row, 0.6), getPercentile(0, row, 0.7), getPercentile(0, col, 0.1), getPercentile(0, col, 0.2))
    return grids
