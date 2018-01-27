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
        self.attacker = None

    def to_json(self):
        """ convert object to dictionary """
        json_tower = {}
        json_tower["id"] = self.id
        json_tower["playerId"] = self.playerId
        json_tower["coord"] = self.coord
        json_tower["unitsCount"] = self.unitsCount
        json_tower["counter"] = self.counter
        json_tower["isAttacked"] = self.isAttacked
        json_tower["hp"] = self.hp
        json_tower["attacker"] = self.attacker
        return json_tower
