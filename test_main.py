from Engine import Engine

en = Engine()
player = en.spawn_player()
print(en.towers)
print(en.players)
print(en.hqs)
# print(en.arena)
# to get player map:
# en.players[1].playerMap