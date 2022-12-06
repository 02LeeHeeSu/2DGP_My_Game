from pico2d import *
import math

import game_framework
import game_world
import server

from define_dir import up, down, right, left
from define_PPM import Pixel_Per_Sec_chu
from depth import level

import random
from BehaviorTree import BehaviorTree, Leaf

Time_Per_Move = 1.0
Move_Per_Time = 1.0 / Time_Per_Move
FPMove = 16


def absolute(a):
    if a >= 0:
        return a
    else:
        return -a


def calculate_distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


animation_names = ['move']


class ChuChu:
    images = None
    hit_sound = None

    def __init__(self):
        self.x = random.randint(40 + 192 * 2 + 45 + 1, server.bg.w - 40 - 192 * 2 - 45 - 1)
        self.y = random.randint(55 + 192 * 2 + 60 + 1, server.bg.h - 55 - 192 * 2 - 60 - 1)
        self.tx, self.ty = self.x, self.y
        self.load_images()
        self.dir = random.randint(up, left)
        self.speed = Pixel_Per_Sec_chu
        self.timer = 1.0
        self.frame = 0
        self.build_behavior_tree()
        if ChuChu.hit_sound is None:
            ChuChu.hit_sound = load_wav('Sound/Enemy/Enemy_Hit.wav')

    def update(self):
        self.bt.run()

        self.timer -= game_framework.frame_time

        self.frame = (self.frame + FPMove * Move_Per_Time * game_framework.frame_time) % FPMove

        if self.dir == up:
            self.y += self.speed * game_framework.frame_time
        elif self.dir == down:
            self.y -= self.speed * game_framework.frame_time
        elif self.dir == right:
            self.x += self.speed * game_framework.frame_time
        elif self.dir == left:
            self.x -= self.speed * game_framework.frame_time

        self.x = clamp(192 + 40, self.x, server.bg.w - 192 - 40)
        self.y = clamp(192 + 55, self.y, server.bg.h - 192 - 55)

    def draw(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        ChuChu.images['move'][int(self.frame)].draw(sx, sy, 80, 105)

    def load_images(self):
        if ChuChu.images is None:
            ChuChu.images = {}
            for name in animation_names:
                ChuChu.images[name] = [load_image("Monsters/Chu_Chu/" + name + "%d" % i + ".png") for i in range(1, 16 + 1)]

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        return sx - 40, sy - 52.5, sx + 40, sy + 52.5

    def handle_collision(self, other, group):
        if group == 'Sword:Monster':
            ChuChu.hit_sound.play()
            if self in game_world.world[level['Monsters']]:
                game_world.remove_object(self, level['Monsters'])
        if group == 'Arrow:Monster':
            ChuChu.hit_sound.play()
            if self in game_world.world[level['Monsters']]:
                game_world.remove_object(self, level['Monsters'])
        if group == 'Shield:Monster':
            if self.dir == up:
                self.y -= 100
                self.y = clamp(192 + 60, self.y, server.bg.h - 192 - 60)
            elif self.dir == down:
                self.y += 100
                self.y = clamp(192 + 60, self.y, server.bg.h - 192 - 60)
            elif self.dir == right:
                self.x -= 100
                self.x = clamp(192 + 45, self.x, server.bg.w - 192 - 45)
            elif self.dir == left:
                self.x += 100
                self.x = clamp(192 + 45, self.x, server.bg.w - 192 - 45)
        if group == 'Rock:ChuChu':
            self.speed = 0
    
    def look_random(self):
        self.tx = random.randint(40 + 192 * 2 + 45 + 1, server.bg.w - 40 - 192 * 2 - 45 - 1)
        self.ty = random.randint(55 + 192 * 2 + 60 + 1, server.bg.h - 55 - 192 * 2 - 60 - 1)
        dx = self.tx - self.x
        dy = self.ty - self.y

        if dx >= 0 and dy >= 0:
            if dx >= dy:
                self.dir = right
            else:
                self.dir = up

        if dx >= 0 > dy:
            dy = absolute(dy)

            if dx >= dy:
                self.dir = right
            else:
                self.dir = down

        if dx < 0 <= dy:
            dx = absolute(dx)

            if dx >= dy:
                self.dir = left
            else:
                self.dir = up

        if dx < 0 and dy < 0:
            dx = absolute(dx)
            dy = absolute(dy)

            if dx >= dy:
                self.dir = left
            else:
                self.dir = down

    def move_to_random(self):
        if self.timer <= 0:
            self.look_random()
            self.timer = 1.0
            return BehaviorTree.SUCCESS

        return BehaviorTree.FAIL

    def build_behavior_tree(self):
        move_node = Leaf('move to random position', self.move_to_random)

        self.bt = BehaviorTree(move_node)
