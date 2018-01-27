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
        self.isDead = False
        self.currentID = 1 # TODO: Any better approach to keep track of next player ID?
        self.HQCoords = [(20, 7), (20, 40), (7, 25), (35, 12), (42, 35)]
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
        self.update_map()
        return player

    def update(self):
        # movement: including units collapsing
        # map visibility: units, hqs, towers
        # attack notification
        self.update_map()
        for player in self.players:
            player.update()

    def issue_command(self, playerId, units, target):
        self.players[playerId].issue_command(units, target)
    
    def update_map(self):
        self.arena = [[C.EMPTY for i in range(C.COL)] for j in range(C.ROW)]
        for key, value in self.players.items():
            for key, unit in value.units.items():
                self.arena[unit.coord[0]][unit.coord[1]] = [C.UNIT, key, unit.id]
            for tower in value.towers:
                self.arena[tower.coord[0]][tower.coord[1]] = [C.TOWER, key, tower.id]
            for hq in value.hqs:
                self.arena[hq.coord[0]][hq.coord[1]] = [C.HQ, key, hq.id]

        for key, value in self.towers.items():
            self.arena[value.coord[0]][value.coord[1]] = [C.TOWER, C.NEUTRAL_UNIT, value.id]