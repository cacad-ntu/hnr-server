class Constants:
    # arena size
    ROW = 50
    COL = 50
    INITIAL_MINIMUM_EMPTY_RADIUS = 6
    MARGIN = 3
    
    # objects
    NEUTRAL_UNIT = -1
    EMPTY = [0, NEUTRAL_UNIT, NEUTRAL_UNIT]

    # object types
    EMPTY_CELL = 0
    HQ = 1
    TOWER = 2
    UNIT = 3

    # directions
    BOTTOM_RIGHT = 0
    TOP_RIGHT = 1
    TOP = 2
    TOP_LEFT = 3
    BOTTOM_LEFT = 4
    BOTTOM = 5


    MIN_PLAYERS = 3
    

    TOWERS_COUNT = 5
    TOWER_POINTS = 10
    STARTING_UNITS_COUNT = 6
    HQ_POINTS = 15
    POINT_TICKS = 7
    
    HQ_POPULATION = 12
    TOWER_POPULATION = 6
    INITIAL_POPULATION = 6
    
    UNIT_SIGHT_RADIUS = 2
    TOWER_SIGHT_RADIUS = 4
    HQ_SIGHT_RADIUS = 5

    VISIBLE = True
    NOT_VISIBLE = False

    NEW_UNIT_TICKS = 7

    HQ_HP = 30
    TOWER_HP = 15