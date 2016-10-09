# Game Constant

class GameConstant:

    # Grid Type
    FOW = -1
    NON_WALL = 0
    WALL = 1

    # Hive IDs
    EMPTY_HIVE = 9
    PLAYER_HIVE = 10

    # Ownership
    EMPTY = -1

    # Game
    RESPAWN = 3
    ATTACK_RANGE = 1
    VISION_RANGE = 3
    VISION_RANGE_FOREST = 1
    VISION_RANGE_TOWER = 6
    TURN_LIMIT = 100

    # FOW
    HIDDEN = -1
    REVEALED = 1

    # Winning conditions
    WINCON_WIPEOUT = "By Wipeout"
    WINCON_HIVESCORE = "By Base Control"
    WINCON_UNITSCORE = "By Unit Control"
    WINCON_TIE = "Tie"
