from Constants import Constants as C
class HQ:
    def __init__(self, id, playerId, coord):
        self.id = id
        self.playerId = playerId
        self.coord = coord
        self.isAttacked = False
        self.hp = C.HQ_HP
        self.attacker = None