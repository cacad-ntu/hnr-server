from Unit import Unit
from Tower import Tower
from HQ import HQ
from Constants import Constants as C

class Player:
    def __init__(self, id, units, towers, hq, population, capacity, playerMap, initialHQCoord):
        self.id = id
        self.units = units
        self.towers = towers # in most cases should be empty first
        self.hqs = hq
        self.population = population
        self.capacity = capacity
        self.playerMap = playerMap
        self.init_hq(initialHQCoord)
        self.init_units()
        self.update_vision()
        self.unitId = C.STARTING_UNITS_COUNT


    def init_units(self):
        for i in range(C.STARTING_UNITS_COUNT):
            # TODO: spawn units here
            # TODO: how to get new coord for each unit?
            unit = Unit(i, self.id, self.hqs[0].coord, None)
            self.units.append(unit)
            # def __init__(self, unitId, playerId, coord, command):

    def init_hq(self, initialHQCoord):
        if(len(self.hqs) != 0):
            return
        hq = HQ(self.id, self.id, initialHQCoord)
        self.hqs.append(hq)

    def restart_vision(self):
        self.playerMap = [[C.NOT_VISIBLE for col in range(C.COL)] for row in range(C.ROW)]
        
    def update_vision(self):
        # get coords that are visible for each hq, unit and tower
        # set each coord as visible
        self.restart_vision()
        for i in self.hqs:
            self.playerMap[i.coord[0]][i.coord[1]] = C.VISIBLE
        for i in self.towers:
            self.playerMap[i.coord[0]][i.coord[1]] = C.VISIBLE
        for i in self.units:
            self.playerMap[i.coord[0]][i.coord[1]] = C.VISIBLE

    
    def issue_command(self, units, command):
        #TODO
        pass

    def update(self):
        # TODO: update logic
        for unit in self.units:
            unit.update()