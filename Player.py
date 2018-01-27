from Unit import Unit
from Tower import Tower
from HQ import HQ
from Constants import Constants as C

class Player:
    def __init__(self, id, units, towers, hq, population, capacity, playerMap, initialHQCoord, grids):
        self.id = id
        self.units = units
        self.towers = towers # in most cases should be empty first
        self.hqs = hq
        self.population = population
        self.capacity = capacity
        self.playerMap = playerMap
        self.isDead = False
        self.grids = grids
        self.init_hq(initialHQCoord)
        self.update_vision()
        self.unitId = C.STARTING_UNITS_COUNT
        

    def add_unit(self, coord):
        newId = len(self.units)
        unit = Unit(newId, self.id, coord, None)
        self.units[newId] = unit
        return newId     
        

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
            sight = self.grids.cells_within_distance(i.coord, 1)
            for cell in sight:
                self.playerMap[cell[0]][cell[1]]= C.VISIBLE
        for i in self.towers:
            sight = self.grids.cells_within_distance(i.coord, 1)
            for cell in sight:
                self.playerMap[cell[0]][cell[1]]= C.VISIBLE
        for key, i in self.units.items():
            sight = self.grids.cells_within_distance(i.coord, 1)
            for cell in sight:
                self.playerMap[cell[0]][cell[1]]= C.VISIBLE
    
    def issue_command(self, units, target):
        for id in units:
            self.units[id].target = target
    
    def kill_unit(self, unitId):
        self.units[unitId].isDead = True

    def update(self, arena):
        for key, unit in self.units.items():
            if(unit.target == None):
                continue
            haveToMove = True
            objectType = arena[unit.target[0]][unit.target[1]][0]
            if(self.grids.isNeighbour(unit.coord, unit.target) and \
            (objectType == C.HQ or objectType == C.TOWER)):
                haveToMove = False
            if(haveToMove):
                direction = self.grids.get_move(unit.coord, unit.target, self.id, arena)
                self.units[key].coord = self.grids.move(unit.coord, direction)
            unit.update()