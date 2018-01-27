from Player import Player
from Unit import Unit
from HQ import HQ
from Tower import Tower
from Constants import Constants as C
from Grid import Grid

class Engine:
    def __init__(self):
        # init values
        self.players = {}
        self.towers = {}
        self.hqs = {}
        self.grids = Grid(C.COL, C.ROW)
        self.arena = None # get arena with size (row, col) TODO: Eric
        self.currentID = 1 # TODO: Any better approach to keep track of next player ID?
        self.HQCoords = [(1, 1), (6, 1), (7, 25), (35, 12), (42, 35)]
        self.TowerCoords = [(20, 15), (7, 15), (28, 25), (28, 45), (37, 25)]
        
        # building arena
        self.spawn_tower()
        self.update_map()

    def get_next_tower_coord(self):
        # TODO: proper implementation please
        return self.TowerCoords[len(self.towers)]

    def get_next_hq_coord(self):
        # TODO: proper implementation please
        return self.HQCoords[len(self.hqs)]

    def spawn_tower(self):
        # TODO: spawn neutral towers, add neutral units
        for i in range(C.TOWERS_COUNT):
            towerCoord = self.get_next_tower_coord()
            tower = Tower(i, C.NEUTRAL_UNIT, towerCoord, C.TOWER_POPULATION)
            self.towers[i] = tower

    def spawn_player(self):
        # TODO: add new player, units, and hq
        newID = self.currentID
        self.currentID += 1
        player = Player(newID, {}, [], [], C.INITIAL_POPULATION, C.HQ_POPULATION, None, self.get_next_hq_coord(), self.grids)
        self.players[newID] = player
        self.hqs[newID] = player.hqs[0]
        for i in range(C.STARTING_UNITS_COUNT):
            self.spawn_unit(newID)
        self.update_map()
        return player

    def spawn_unit(self, playerId):
        area = self.grids.cells_within_distance(self.players[playerId].hqs[0].coord, 1)
        counter = 0
        for cell in area:
            if(cell == self.players[playerId].hqs[0].coord or self.arena[cell[0]][cell[1]][0] != 0):
                continue
            # TODO: if starting units are more than 6, please fix this logic
            newId = self.players[playerId].add_unit(cell)
            self.arena[cell[0]][cell[1]] = [C.UNIT, playerId, newId]

    def update(self):
        # movement: including units collapsing
        # map visibility: units, hqs, towers
        # attack notification
        for key, value in self.players.items():
            value.update()
        self.update_map()
        self.update_vision()

    def issue_command(self, playerId, units, target):
        self.players[playerId].issue_command(units, target)

    def update_vision(self):
        for playerKey, player in self.players.items():
            if(player.isDead):
                continue
                player.update_vision()
    
    def update_map(self):
        self.arena = [[C.EMPTY for i in range(C.COL)] for j in range(C.ROW)]
        for playerKey, player in self.players.items():
            if(player.isDead):
                continue
            for unitKey, unit in player.units.items():
                if(unit.isDead):
                    continue
                # check for clash
                currentObject = self.arena[unit.coord[0]][unit.coord[1]][0]
                currentOwner = self.arena[unit.coord[0]][unit.coord[1]][1]
                currentId = self.arena[unit.coord[0]][unit.coord[1]][2]
                
                if(currentObject == 0):
                    self.arena[unit.coord[0]][unit.coord[1]] = [C.UNIT, playerKey, unit.id]
                elif(currentObject == C.UNIT):
                    if(currentOwner != playerKey):
                        # kill both units
                        player.kill_unit(unit.id)
                        self.players[currentOwner].kill_unit(currentId)
                    else: # need to check here?
                        pass
                elif(currentObject == C.TOWER):
                    pass
                else:
                    # HQ
                    pass
                
            for tower in player.towers:
                self.arena[tower.coord[0]][tower.coord[1]] = [C.TOWER, playerKey, tower.id]
            for hq in player.hqs:
                self.arena[hq.coord[0]][hq.coord[1]] = [C.HQ, playerKey, hq.id]

        for key, value in self.towers.items():
            self.arena[value.coord[0]][value.coord[1]] = [C.TOWER, C.NEUTRAL_UNIT, value.id]