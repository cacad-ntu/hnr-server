from Constants import Constants as C
class HQ:
    def __init__(self, id, playerId, coord):
        self.id = id
        self.playerId = playerId
        self.coord = coord
        self.isAttacked = False
        self.hp = C.HQ_HP
        self.attacker = None

    def to_json(self):
        """ convert object to dictionary """
        json_hq = {}
        json_hq["id"] = self.id
        json_hq["playerId"] = self.playerId
        json_hq["coord"] = self.coord
        json_hq["isAttacked"] = self.isAttacked
        json_hq["hp"] = self.hp
        json_hq["attacker"] = self.attacker
        return json_hq