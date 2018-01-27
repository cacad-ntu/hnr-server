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
        self.grids = grids
        self.init_hq(initialHQCoord)
        self.init_units()
        self.update_vision()
        self.unitId = C.STARTING_UNITS_COUNT
        

    def init_units(self):
        area = self.grids.cells_within_distance(self.hqs[0].coord, 1)
        counter = 0
        for cell in area:
            if(cell == self.hqs[0].coord):
                continue
            # TODO: if starting units are more than 6, please fix this logic
            unit = Unit(counter, self.id, [cell[0], cell[1]], None)
            self.units[counter] = unit
            counter += 1
            if(counter == C.STARTING_UNITS_COUNT):
                break
        

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
        for unit in units:
            pass

    def update(self):
        # TODO: update logic
        for unit in self.units:
            unit.update()