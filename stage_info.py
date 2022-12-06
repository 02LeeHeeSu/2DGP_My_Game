import game_world

import server

from depth import level

from chuchu import ChuChu
from octorok import Octorok
from vaati import Vaati
from eye import Eye

monsters_info = [[[], [], []],
                 [[], [], []],
                 [[], [], []]]

got_item_info = [[False, False, False],
                 [False, False, False],
                 [False, False, False]]

left, bottom = 0, 0
center = 1
right, top = 2, 2

cur_room = [left, bottom]


def init_stage():
    global cur_room, got_item_info
    cur_room = [left, bottom]
    got_item_info = [[False, False, False],
                     [False, False, False],
                     [False, False, False]]

    init_monsters_info()
    add_monsters()


def init_monsters_info():
    monsters_info[left][bottom] = [ChuChu() for i in range(3)]
    monsters_info[left][center] = [Octorok() for i in range(3)]
    monsters_info[left][top] = [Eye() for i in range(3)]
    monsters_info[center][top] = [ChuChu(), Octorok(), Eye()]
    monsters_info[right][top] = [Octorok(), Octorok(), Eye(), Eye(), Eye()]
    monsters_info[right][center] = [ChuChu() for i in range(8)]
    monsters_info[right][bottom] = [Octorok() for i in range(6)]
    monsters_info[center][bottom] = [ChuChu(), ChuChu(), Octorok(), Octorok(), Eye(), Eye(), Eye(), Eye()]
    monsters_info[center][center] = [Vaati()]


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

        elif type(monster) is Eye:
            game_world.add_collision_group(monster, None, 'Eye:Sphere')
