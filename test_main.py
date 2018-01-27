from Engine import Engine

en = Engine()
player = en.spawn_player()
print(en.towers)
print(en.players)
print(en.hqs)
# for key, unit in en.players[1].units.items():
#     print(unit.coord)


# print(en.arena)
# to get player map:
# area = en.players[1].playerMap
# for i in range(50):
#     for j in range(50):
#         if(area[i][j]):
#             print(i, j)
# en.update_map()
# print("HAHAHA")
# for i in range(50):
#     for j in range(50):
#         if(en.arena[i][j][0] != 0):
#             print(i, j, end="")
#             print(en.arena[i][j])