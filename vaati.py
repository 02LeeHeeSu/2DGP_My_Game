from pico2d import *
import random

import game_framework
import game_world
import server

from eye import Eye

from define_PPM import Pixel_Per_Sec_vaati
from depth import level

from BehaviorTree import BehaviorTree, Leaf

Move_Per_Time = 1.0
Time_Per_Move = 1.0 / Move_Per_Time
FPMove = 12

Teleport_Per_Time = 2.0
Time_Per_Teleport = 1.0 / Teleport_Per_Time
FPTeleport = 8


animation_names = ['move', 'teleport']


def absolute(a):
    if a >= 0:
        return a
    else:
        return -a


class Vaati:
    images = None

    def __init__(self):
        self.weakness = load_image('Monsters/Vaati/weakness.png')
        self.hp = 20
        self.x, self.y = server.bg.w // 2, server.bg.h // 2
        self.load_images()
        self.speed = Pixel_Per_Sec_vaati
        self.tp_timer = 2.0
        self.motion_timer = Time_Per_Teleport
        self.Teleport = False
        self.is_stopped = False
        self.frame_move = 0
        self.frame_teleport = 0
        self.build_behavior_tree()
        self.hit_sound = load_wav('Sound/Enemy/Enemy_Hit.wav')
        self.teleport_sound = load_wav('Sound/Enemy/Vaati_Teleport.wav')
        self.eye_summon_sound = load_wav('Sound/Enemy/Vaati_EyeSummon.wav')

    def update(self):
        self.bt.run()

        self.tp_timer -= game_framework.frame_time

        if self.tp_timer <= Teleport_Per_Time:
            if not self.Teleport:
                self.teleport_sound.play()
            self.Teleport = True
            self.is_stopped = True
        else:
            self.Teleport = False
            self.is_stopped = False

        self.frame_move = (self.frame_move + FPMove * Move_Per_Time * game_framework.frame_time) % FPMove

        if self.Teleport:
            self.motion_timer -= game_framework.frame_time
            self.frame_teleport = (self.frame_teleport + FPTeleport * Teleport_Per_Time * game_framework.frame_time) % FPTeleport

        self.x = clamp(192 + 110, self.x, server.bg.w - 192 - 110)
        self.y = clamp(192 + 135, self.y, server.bg.h - 192 - 135)

        if self.hp <= 0:
            game_world.remove_object(self, level['Monsters'])

    def draw(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        if self.Teleport:
            Vaati.images['teleport'][int(self.frame_teleport)].draw(sx, sy, 220, 270)
        else:
            Vaati.images['move'][int(self.frame_move)].draw(sx, sy, 220, 270)

        if self.is_stopped:
            self.weakness.draw(sx, sy - 50, 60, 110)

    def load_images(self):
        if Vaati.images is None:
            Vaati.images = {}
            Vaati.images['move'] = [load_image("Monsters/Vaati/" + 'move' + "%d" % i + ".png") for i in range(1, 12 + 1)]
            Vaati.images['teleport'] = [load_image("Monsters/Vaati/" + 'teleport' + "%d" % i + ".png") for i in range(1, 8 + 1)]

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        if self.is_stopped:
            return sx - 30, sy - 110 - 10, sx + 30, sy - 10

        return sx - 110, sy - 135, sx + 110, sy + 135

    def handle_collision(self, other, group):
        if group == 'Sword:Monster':
            if self.is_stopped:
                self.hit_sound.play()
                self.hp -= 1
                self.is_stopped = False
        if group == 'Arrow:Monster':
            if self.is_stopped:
                self.hit_sound.play()
                self.hp -= 1

    # AI
    def create_eye(self):
        self.eye_summon_sound.play()
        eyes = [Eye() for i in range(2)]
        game_world.add_objects(eyes, level['Monsters'])
        for eye in eyes:
            game_world.add_collision_group(eye, None, 'eye:Sphere')
            game_world.add_collision_group(None, eye, 'Link:Monster')
            game_world.add_collision_group(None, eye, 'Sword:Monster')
            game_world.add_collision_group(None, eye, 'Arrow:Monster')
            game_world.add_collision_group(None, eye, 'Shield:Monster')

    def teleport_random(self):
        if self.tp_timer <= 0.0:
            self.tp_timer = 6.0

            self.is_stopped = False

            self.x = random.randint(192 + 110, server.bg.w - 192 - 110)
            self.y = random.randint(192 + 135, server.bg.h - 192 - 135)

            self.create_eye()

            return BehaviorTree.SUCCESS

        return BehaviorTree.FAIL

    def build_behavior_tree(self):
        tp_node = Leaf('teleport random location', self.teleport_random)

        self.bt = BehaviorTree(tp_node)

