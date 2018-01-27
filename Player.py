from Unit import Unit
from Tower import Tower
from HQ import HQ
from Constants import Constants as C

class Player:
    def __init__(self, id, units, towers, hq, population, capacity, playerMap, initialHQCoord, grids):
        self.id = id
        self.units = units # dictionary
        self.towers = towers # in most cases should be empty first
        self.hqs = hq # list of hq objects
        self.population = population
        self.capacity = capacity
        self.playerMap = playerMap
        self.isDead = False
        self.grids = grids
        self.init_hq(initialHQCoord)
        self.update_vision()
        self.unitId = C.STARTING_UNITS_COUNT
        self.points = 0
        

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
            sight = self.grids.cells_within_distance(i.coord, C.HQ_SIGHT_RADIUS)
            for cell in sight:
                self.playerMap[cell[0]][cell[1]]= C.VISIBLE
        for i in self.towers:
            sight = self.grids.cells_within_distance(i.coord, C.TOWER_SIGHT_RADIUS)
            for cell in sight:
                self.playerMap[cell[0]][cell[1]]= C.VISIBLE
        for key, i in self.units.items():
            sight = self.grids.cells_within_distance(i.coord, C.UNIT_SIGHT_RADIUS)
            for cell in sight:
                self.playerMap[cell[0]][cell[1]]= C.VISIBLE

    def remove_tower(self, towerId):
        removeIndex = 0
        for i in range(len(self.towers)):
            if(self.towers[i].id == towerId):
                removeIndex = i
                break
        print("To be removed", removeIndex, " len ", len(self.towers))
        self.towers.pop(removeIndex)
        print("New len ", len(self.towers))
    def update_points(self):
        self.points += len(self.hqs) * C.HQ_POINTS + len(self.towers) * C.TOWER_POINTS
    
    def issue_command(self, units, target):
        for id in units:
            self.units[id].target = target
    
    def kill_unit(self, unitId):
        self.units[unitId].isDead = True
        self.population -= 1

    def recalculate_capacity(self):
        self.capacity = len(self.hqs) * C.HQ_POPULATION + len(self.towers) * C.TOWER_POPULATION

    def update(self, arena):
        #TODO: Boundary Check
        self.recalculate_capacity()
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
                newCoord = self.grids.move(unit.coord, direction)
                if(newCoord == self.units[key].prevPos):
                    self.units[key].stuckedCounter += 1
                else:
                    self.units[key].stuckedCounter = 0
                if(self.units[key].stuckedCounter == C.STUCKED_TOLERANCE):
                    self.units[key].target = None
                else:
                    self.units[key].prevPos = self.units[key].coord
                    self.units[key].coord = newCoord
                    if(newCoord[0] < 0 or newCoord[0] >= C.COL or newCoord[1] < 0 or newCoord[1] >= C.ROW):
                        continue
                    arena[newCoord[0]][newCoord[1]] = [C.UNIT, self.id, key]
                # unit = self.units[key]
                # if(len(unit.path) > unit.pathIndex and self.grids.is_free(unit.path[unit.pathIndex], self.id, arena)):
                #     self.units[key].coord = unit.path[unit.pathIndex]
                #     self.units[key].pathIndex += 1
                # self.grids.bfs(source, target, playerId, arena)
            unit.update()