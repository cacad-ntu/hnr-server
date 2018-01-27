class Constants:
    # arena size
    ROW = 50
    COL = 50

    
    # objects
    NEUTRAL_UNIT = -1
    EMPTY = [0, NEUTRAL_UNIT, NEUTRAL_UNIT]
    HQ = 1
    TOWER = 2
    UNIT = 3

    # directions

    MIN_PLAYERS = 3
    

    TOWERS_COUNT = 5
    TOWER_POINTS = 10
    STARTING_UNITS_COUNT = 6
    HQ_POINTS = 15
    POINT_CLOCK = 10 # in seconds
    
    HQ_POPULATION = 12
    TOWER_POPULATION = 6
    INITIAL_POPULATION = 6
    
    UNIT_SIGHT_RADIUS = 2
    TOWER_SIGHT_RADIUS = 4
    HQ_SIGHT_RADIUS = 5

    VISIBLE = True
    NOT_VISIBLE = False
