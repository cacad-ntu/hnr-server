class Unit:
    def __init__(self, unitId, playerId, coord, target):
        self.id = unitId
        self.playerId = playerId
        self.coord = [coord[0], coord[1]]
        self.target = target
        self.pollCounter = 0
    
    def update(self):
        #TODO: update logic
        pass