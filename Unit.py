class Unit:
    def __init__(self, unitId, playerId, coord, target):
        self.id = unitId
        self.playerId = playerId
        self.coord = [coord[0], coord[1]]
        self.target = target
        self.pollCounter = 0
        self.isDead = False
    
    def update(self):
        if(self.target[0] == self.coord[0] and self.target[1] == self.coord[1]):
            self.target = None