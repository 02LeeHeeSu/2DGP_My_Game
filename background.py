from pico2d import *

import game_framework
import game_world
from canvas_size import width, height

import server

import stage_info
from depth import level

import door
import item


def open_door():
    x, y = stage_info.cur_room[0], stage_info.cur_room[1]
    if item.Item_Queue and not stage_info.got_item_info[x][y]:
        stage_info.got_item_info[x][y] = True
        dropped_item = item.Item()
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
        self.is_in_boss_room = False
        self.low_health_timer = 1.0
        self.Musics = [load_music('Sound/Background/Main_BGM.mp3'),
                       load_music('Sound/Background/Boss_BGM.mp3'),
                       load_wav('Sound/Background/LowHealth.wav')]
        for i in range(2):
            self.Musics[i].set_volume(100)
        self.Musics[2].set_volume(72)
        self.Musics[0].repeat_play()

    def update(self):
        self.low_health_timer -= game_framework.frame_time

        self.window_left = clamp(0, int(server.link.x) - width // 2, self.w - width - 1)
        self.window_bottom = clamp(0, int(server.link.y) - height // 2, self.h - height - 1)

        if stage_info.monsters_info[self.x][self.y]:
            stage_info.add_monsters()

        if not game_world.world[level['Monsters']] and not door.is_opened_door:
            door.is_opened_door = True
            open_door()

        if stage_info.cur_room == [stage_info.center, stage_info.center] and not self.is_in_boss_room:
            self.is_in_boss_room = True
            self.Musics[0].stop()
            self.Musics[1].repeat_play()

        if server.link.cur_hp <= server.link.max_hp / 3 and self.low_health_timer <= 0.0:
            self.low_health_timer = 1.0
            self.Musics[2].play()
    def draw(self):
        self.image[self.x][self.y].clip_draw_to_origin(self.window_left, self.window_bottom,
                                                       width, height,
                                                       0, 0)

    def handle_event(self, event):
        pass
