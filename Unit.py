class Unit:
    def __init__(self, unitId, playerId, coord, command):
        self.id = unitId
        self.playerId = playerId
        self.coord = [coord[0], coord[1]]
        self.command = command
        self.pollCounter = 0
    
    def update(self):
        #TODO: update logic
        pass