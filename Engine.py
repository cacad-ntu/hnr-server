from Player import Player
from Unit import Unit
from HQ import HQ
from Tower import Tower
from Constants import Constants as C
from Grid import Grid
from random import randint

class Engine:
    def __init__(self):
        # init values
        self.players = {}
        self.towers = {}
        self.hqs = {}
        self.grids = Grid(C.COL, C.ROW)
        self.arena = [[C.EMPTY for i in range(C.COL)] for j in range(C.ROW)]
        self.currentID = 1 # TODO: Any better approach to keep track of next player ID?
        self.HQCoords = [(1, 1), (6, 1), (7, 25), (35, 12), (42, 35)]
        self.TowerCoords = [(20, 15), (7, 15), (28, 25), (28, 45), (37, 25)]
        self.newUnitCounter = C.NEW_UNIT_TICKS
        self.pointCounter = C.POINT_TICKS

        # Flags
        self.use_bfs = False

        # building arena
        self.spawn_tower()
        self.update_map()

    def get_all_towers(self):
        """ get all towers in form of dictionary """
        json_towers = []
        for tower in self.towers.values():
            if not tower:
                continue
            json_towers.append(tower.to_json())
        return json_towers

    def get_all_hqs(self):
        """ get all hqs in form of dictionary """
        json_hqs = []
        for hq in self.hqs.values():
            if not hq:
                continue
            json_hqs.append(hq.to_json())
        return json_hqs

    def get_next_empty_coord(self,max_dist):
        for i in range(50):
            col = randint(0+C.MARGIN,C.COL-1-C.MARGIN)
            row = randint(0+C.MARGIN,C.ROW-1-C.MARGIN)

            cells = self.grids.cells_within_distance(tuple([col,row]),max_dist)

            isEmpty = True

            for it in cells:

                if self.arena[it[0]][it[1]][0] != C.EMPTY_CELL:
                    isEmpty = False

            if isEmpty: return tuple([col,row])

        return self.get_next_empty_coord(max_dist-1)

    def get_next_tower_coord(self):
        return self.get_next_empty_coord(C.INITIAL_MINIMUM_EMPTY_RADIUS)

    def get_next_hq_coord(self):
        return self.get_next_empty_coord(C.INITIAL_MINIMUM_EMPTY_RADIUS)

    def get_sorted_players(self):
        """ get player tops player """
        sorted_players = sorted(self.players.values(), key=lambda x: x.points, reverse=True)

        list_sorted = []
        for player in sorted_players:
            if player.isDead:
                continue
            list_sorted.append({"player_id": player.id, "points": player.points})
        return list_sorted

    def toggle_bfs(self, value):
        """ Toggle use_bfs flag """
        self.use_bfs = value

    def spawn_tower(self):
        # TODO: spawn neutral units
        for i in range(C.TOWERS_COUNT):
            towerCoord = self.get_next_tower_coord()
            tower = Tower(i, C.NEUTRAL_UNIT, towerCoord, C.TOWER_POPULATION)
            self.towers[i] = tower

    def spawn_player(self):
        newID = self.currentID
        self.currentID += 1
        player = Player(newID, {}, [], [], 0, C.HQ_POPULATION, None, self.get_next_hq_coord(), self.grids)
        self.players[newID] = player
        self.hqs[newID] = player.hqs[0]
        for i in range(C.STARTING_UNITS_COUNT):
            self.spawn_unit(newID)
        self.update_map()
        return player

    def remove_player(self, id):
        self.players[id].isDead = True
        self.cleanup_player(id)

    def cleanup_player(self, id):
        for hq in self.players[id].hqs:
            self.hqs[hq.id] = None
        for tower in self.players[id].towers:
            self.towers[tower.id].playerId = C.NEUTRAL_UNIT
            self.towers[tower.id].hp = C.TOWER_HP


    def spawn_unit(self, playerId):
        if(self.players[playerId].population == self.players[playerId].capacity):
            return
        currentRadius = 1
        flag = True
        while(flag):
            area = self.grids.cells_within_distance(self.players[playerId].hqs[0].coord, currentRadius)
            innerArea = []
            if(currentRadius > 1):
                innerArea = self.grids.cells_within_distance(self.players[playerId].hqs[0].coord, currentRadius - 1)
                for i in innerArea:
                    if i in area:
                        area.remove(i)
            for cell in area:
                objectType = self.arena[cell[0]][cell[1]][0]
                owner = self.arena[cell[0]][cell[1]][1]
                objectId = self.arena[cell[0]][cell[1]][2]
                if(objectType == C.UNIT and owner != playerId):
                    # kill enemy unit
                    self.players[owner].kill_unit(objectId)
                    continue
                if(cell == self.players[playerId].hqs[0].coord or objectType != C.EMPTY_CELL):
                    continue
                newId = self.players[playerId].add_unit(cell)
                self.arena[cell[0]][cell[1]] = [C.UNIT, playerId, newId]
                flag = False
                break
            currentRadius += 1
        self.players[playerId].population += 1

    def update(self):
        # movement: including units collapsing
        # map visibility: units, hqs, towers
        # attack notification

        # check for buildings being attacked
        self.update_attack_progress()

        for key, value in self.players.items():
            if(value.isDead):
                continue
            value.update(self.arena, self.use_bfs)
        self.update_map()
        self.newUnitCounter -= 1
        self.pointCounter -= 1
        if(self.newUnitCounter == 0):
            self.spawn_new_units()
            self.newUnitCounter = C.NEW_UNIT_TICKS
        if(self.pointCounter == 0):
            self.update_points()
            self.pointCounter = C.POINT_TICKS
        self.update_vision()

    def issue_command(self, playerId, units, target):
        self.players[playerId].issue_command(units, target, self.arena)

    def spawn_new_units(self):
        for playerKey, player in self.players.items():
            if(player.isDead):
                continue
            self.spawn_unit(playerKey)

    def update_vision(self):
        for playerKey, player in self.players.items():
            if(player.isDead):
                continue
            player.update_vision()

    def update_map(self):
        self.arena = [[C.EMPTY for i in range(C.COL)] for j in range(C.ROW)]
        for key, value in self.towers.items():
            self.arena[value.coord[0]][value.coord[1]] = [C.TOWER, C.NEUTRAL_UNIT, value.id]
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

    def update_attack_progress(self):
        for towerKey, tower in self.towers.items():
            self.towers[towerKey].isAttacked = False
        for hqKey, hq in self.hqs.items():
            if(hq == None):
                continue
            self.hqs[hqKey].isAttacked = False

        for playerKey, player in self.players.items():
            if(player.isDead):
                continue
            for unitKey, unit in player.units.items():
                if(unit.target == None or unit.isDead):
                    continue
                if(self.grids.isNeighbour(unit.coord, unit.target)):
                    objectType = self.arena[unit.target[0]][unit.target[1]][0]
                    owner = self.arena[unit.target[0]][unit.target[1]][1]
                    objectId = self.arena[unit.target[0]][unit.target[1]][2]
                    if(objectType == C.TOWER and owner != playerKey):
                        self.towers[objectId].isAttacked = True
                        self.towers[objectId].attacker = playerKey
                        # change ownership

                        if(self.towers[objectId].hp == 0):
                            if(owner != C.NEUTRAL_UNIT and self.towers[objectId] in self.players[owner].towers):
                                # self.players[owner].towers.remove(self.towers[objectId])
                                self.players[owner].remove_tower(objectId)
                            self.towers[objectId].playerId = playerKey
                            self.players[playerKey].towers.append(self.towers[objectId])
                            self.towers[objectId].hp = C.TOWER_HP
                            self.arena[unit.target[0]][unit.target[1]] = [C.TOWER, playerKey, objectId]

                    if(objectType == C.HQ and owner != playerKey):
                        self.hqs[objectId].isAttacked = True
                        self.hqs[objectId].attacker = playerKey
                        # change ownership
                        if(self.hqs[objectId].hp == 0):
                            self.hqs[objectId].playerId = playerKey
                            if(self.hqs[objectId] in self.players[owner].hqs):
                                self.players[owner].hqs.remove(self.hqs[objectId])
                            self.players[playerKey].hqs.append(self.hqs[objectId])
                            self.hqs[objectId].hp = C.HQ_HP
                            self.arena[unit.target[0]][unit.target[1]] = [C.HQ, playerKey, objectId]
                            # check player is still alive
                            if(len(self.players[owner].hqs) == 0):
                                self.players[owner].isDead = True
                                self.cleanup_player(owner)


        for towerKey, tower in self.towers.items():
            if(not self.towers[towerKey].isAttacked):
                if(self.towers[towerKey].hp < C.TOWER_HP):
                    self.towers[towerKey].hp += 1
            else:
                self.towers[towerKey].hp -= 1

        for hqKey, hq in self.hqs.items():
            if(hq == None):
                continue
            if(not self.hqs[hqKey].isAttacked):
                if(self.hqs[hqKey].hp < C.HQ_HP):
                    self.hqs[hqKey].hp += 1
            else:
                self.hqs[hqKey].hp -= 1

    def update_points(self):
        for playerKey, player in self.players.items():
            if(player.isDead):
                continue
            player.update_points()