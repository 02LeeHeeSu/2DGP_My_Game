from pico2d import *

import define_dir
import game_world
import item

import server

import stage_info

from define_dir import up, down, right, left
from depth import level

from item import Item

is_opened_door = False

# 1824, 1344
door_place = [(912, 1344 - 132), (912, 132), (1824 - 132, 672), (132, 672)]


door_info = [[[define_dir.up], [define_dir.up, define_dir.down], [define_dir.down, define_dir.right]],
             [[define_dir.up, define_dir.right], [], [define_dir.right, define_dir.left]],
             [[define_dir.up, define_dir.left], [define_dir.up, define_dir.down], [define_dir.down, define_dir.left]]]


def change_room(direction):
    global is_opened_door
    is_opened_door = False

    for obj in game_world.world[level['Objects']]:
        if type(obj) is Item:
            game_world.remove_object(obj, level['Objects'])
            item.Item_Queue.append(obj.item)

    if direction == up:
        stage_info.cur_room[1] += 1
        server.link.x = server.bg.w // 2
        server.link.y = 66 + 192 + 1

    elif direction == down:
        stage_info.cur_room[1] -= 1
        server.link.x = server.bg.w // 2
        server.link.y = server.bg.h - 66 - 192 - 1

    elif direction == right:
        stage_info.cur_room[0] += 1
        server.link.x = 66 + 192 + 1
        server.link.y = server.bg.h // 2

    elif direction == left:
        stage_info.cur_room[0] -= 1
        server.link.x = server.bg.w - 66 - 192 - 1
        server.link.y = server.bg.h // 2

    server.bg.x, server.bg.y = stage_info.cur_room[0], stage_info.cur_room[1]


class Door:
    image = None
    open_sound = None

    def __init__(self, d):
        if Door.image is None:
            Door.image = load_image('Door/door.png')
        self.x, self.y = door_place[d]
        self.d = d
        if Door.open_sound is None:
            Door.open_sound = load_wav('Sound/Objects/DungeonDoor.wav')
        Door.open_sound.play()

    def update(self):
        pass

    def draw(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        if self.d == up:
            self.image.clip_composite_draw(0, 0, 300, 264, 0, 'v', sx, sy, 300, 264)

        elif self.d == down:
            self.image.clip_draw(0, 0, 300, 264, sx, sy)

        if self.d == right:
            self.image.clip_composite_draw(0, 0, 300, 264, 3.141592 / 2.0, '', sx, sy, 300, 264)

        elif self.d == left:
            self.image.clip_composite_draw(0, 0, 300, 264, -3.141592 / 2.0, '', sx, sy, 300, 264)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        return sx - 66, sy - 66, sx + 66, sy + 66

    def handle_collision(self, other, group):
        if group == 'Link:Door':
            game_world.world[level['Door']].clear()
            game_world.collision_group['Link:Door'][1].clear()
            change_room(self.d)
