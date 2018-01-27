from Constants import Constants as C
class Tower:
    def __init__(self, id, playerId, coord, unitsCount):
        self.id = id
        self.playerId = playerId
        self.coord = coord
        self.unitsCount = unitsCount
        self.counter = 0
        self.isAttacked = False
        self.hp = C.TOWER_HP