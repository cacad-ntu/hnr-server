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
            if(i.isDead):
                continue
            sight = self.grids.cells_within_distance(i.coord, C.UNIT_SIGHT_RADIUS)
            for cell in sight:
                self.playerMap[cell[0]][cell[1]]= C.VISIBLE

    def remove_tower(self, towerId):
        removeIndex = 0
        for i in range(len(self.towers)):
            if(self.towers[i].id == towerId):
                removeIndex = i
                break
        self.towers.pop(removeIndex)
    def update_points(self):
        self.points += len(self.hqs) * C.HQ_POINTS + len(self.towers) * C.TOWER_POINTS

    def issue_command(self, units, target, arena):
        for id in units:
            self.units[id].target = target
            self.units[id].path = self.grids.bfs(self.units[id].coord, target, self.id, arena)
            self.units[id].pathIndex = 0


    def kill_unit(self, unitId):
        self.units[unitId].isDead = True
        self.population -= 1

    def recalculate_capacity(self):
        self.capacity = len(self.hqs) * C.HQ_POPULATION + len(self.towers) * C.TOWER_POPULATION

    def update(self, arena, use_bfs=False):
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


                # dfs
                unit = self.units[key]
                if(not(unit.path != None and len(unit.path) > unit.pathIndex and self.grids.is_free(unit.path[unit.pathIndex], self.id, arena))):
                    self.units[key].path = self.grids.dfs(unit.coord, unit.target, self.id, arena)
                    self.units[key].pathIndex = 0    
                if(len(unit.path) > unit.pathIndex):
                    newCoord = unit.path[unit.pathIndex]
                    self.units[key].pathIndex += 1
                    
                """=======
                # bfs
                if use_bfs:
                    unit = self.units[key]
                    if(not(unit.path != None and len(unit.path) > unit.pathIndex and self.grids.is_free(unit.path[unit.pathIndex], self.id, arena))):
                        self.units[key].path = self.grids.bfs(unit.coord, unit.target, self.id, arena)
                        self.units[key].pathIndex = 0
                    if(len(unit.path) > unit.pathIndex):
                        newCoord = unit.path[unit.pathIndex]
                        self.units[key].pathIndex += 1

                >>>>>>> 7d1e03de6d5d3586dd0e5922b66fd3d71a8b6297
                """
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
            unit.update()
