class Tower:
    def __init__(self, id, playerId, coord, unitsCount):
        self.id = id
        self.playerId = playerId
        self.coord = coord
        self.unitsCount = unitsCount
        self.counter = 0
        self.isAttacked = False