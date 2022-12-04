import game_world

import server

from depth import level

from chuchu import ChuChu
from octorok import Octorok

monsters_info = [[[], [], []],
                 [[], [], []],
                 [[], [], []]]

left, bottom = 0, 0
center = 1
right, top = 2, 2

cur_room = [left, bottom]


def init_monsters_info():
    monsters_info[left][bottom] = []
    monsters_info[left][center] = [ChuChu()]
    monsters_info[left][top] = [Octorok()]
    monsters_info[center][top] = [ChuChu(), Octorok()]
    monsters_info[right][top] = [ChuChu() for i in range(3)]
    monsters_info[right][center] = [Octorok() for i in range(3)]
    monsters_info[right][bottom] = [ChuChu(), ChuChu(), ChuChu(), Octorok(), Octorok(), Octorok()]
    monsters_info[center][bottom] = []


def add_monsters():
    while monsters_info[cur_room[0]][cur_room[1]]:
        monster = monsters_info[cur_room[0]][cur_room[1]].pop()
        game_world.add_object(monster, level['Monsters'])
        game_world.add_collision_group(None, monster, 'Link:Monster')
        game_world.add_collision_group(None, monster, 'Sword:Monster')
        game_world.add_collision_group(None, monster, 'Arrow:Monster')
        game_world.add_collision_group(None, monster, 'Shield:Monster')

        if type(monster) is ChuChu:
            game_world.add_collision_group(None, monster, 'Rock:ChuChu')

        elif type(monster) is Octorok:
            game_world.add_collision_group(None, monster, 'Rock:Octorok')
