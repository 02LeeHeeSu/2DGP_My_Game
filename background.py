from pico2d import *

import game_world
from canvas_size import width, height

import server

import stage_info
from depth import level

import door
from item import Item


def open_door():
    if item.Item_Queue:
        dropped_item = Item()
        game_world.add_object(dropped_item, level['Objects'])
        game_world.add_collision_group(None, dropped_item, 'Link:Item')

    for d in door.door_info[stage_info.cur_room[0]][stage_info.cur_room[1]]:
        door_obj = door.Door(d)
        game_world.add_object(door_obj, level['Door'])
        game_world.add_collision_group(None, door_obj, 'Link:Door')


class Background:
    def __init__(self):
        self.image = [[load_image('Background/background_%d%d.png' % (x, y)) for y in range(3)] for x in range(3)]
        self.x, self.y = stage_info.cur_room[0], stage_info.cur_room[1]
        self.w = self.image[self.x][self.y].w
        self.h = self.image[self.x][self.y].h

    def draw(self):
        self.image[self.x][self.y].clip_draw_to_origin(self.window_left, self.window_bottom,
                                                       width, height,
                                                       0, 0)

    def update(self):
        self.window_left = clamp(0, int(server.link.x) - width // 2, self.w - width - 1)
        self.window_bottom = clamp(0, int(server.link.y) - height // 2, self.h - height - 1)

        if stage_info.monsters_info[self.x][self.y]:
            stage_info.add_monsters()

        if not game_world.world[level['Monsters']] and not door.is_opened_door:
            door.is_opened_door = True
            open_door()

    def handle_event(self, event):
        pass
