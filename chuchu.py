from pico2d import *
import math

import game_framework
import game_world
import server

from define_dir import defined_direction
from define_PPM import Pixel_Per_Meter, Pixel_Per_Sec_chu
from depth import level

import random
from BehaviorTree import BehaviorTree, Selector, Sequence, Leaf

from canvas_size import width, height

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

    def load_images(self):
        if ChuChu.images is None:
            ChuChu.images = {}
            for name in animation_names:
                ChuChu.images[name] = [load_image("Monsters/Chu_Chu/" + name + "%d" % i + ".png") for i in range(1, 16 + 1)]

    def get_bb(self):
        return self.x - 40, self.y - 52.5, self.x + 40, self.y + 52.5

    def __init__(self):
        self.x, self.y = 80, 105
        self.tx, self.ty = random.randint(40, width - 40), random.randint(55, height - 55)
        self.load_images()
        self.dir = random.randint(0, 3)
        self.speed = Pixel_Per_Sec_chu
        self.timer = 1.0
        self.frame = 0
        self.build_behavior_tree()
    
    def look_random(self):
        self.tx = random.randint(40, width - 40)
        self.ty = random.randint(55, height - 55)
        dx = self.tx - self.x
        dy = self.ty - self.y

        if dx >= 0 and dy >= 0:
            if dx >= dy:
                self.dir = defined_direction['right']
            else:
                self.dir = defined_direction['up']

        if dx >= 0 > dy:
            dy = absolute(dy)

            if dx >= dy:
                self.dir = defined_direction['right']
            else:
                self.dir = defined_direction['down']

        if dx < 0 <= dy:
            dx = absolute(dx)

            if dx >= dy:
                self.dir = defined_direction['left']
            else:
                self.dir = defined_direction['up']

        if dx < 0 and dy < 0:
            dx = absolute(dx)
            dy = absolute(dy)

            if dx >= dy:
                self.dir = defined_direction['left']
            else:
                self.dir = defined_direction['down']

    def move_to_random(self):
        if self.timer <= 0:
            self.look_random()
            self.timer = 1.0
            return BehaviorTree.SUCCESS

        return BehaviorTree.FAIL

    def build_behavior_tree(self):
        move_node = Leaf('move to random position', self.move_to_random)

        self.bt = BehaviorTree(move_node)

    def update(self):
        self.bt.run()

        self.timer -= game_framework.frame_time

        self.frame = (self.frame + FPMove * Move_Per_Time * game_framework.frame_time) % FPMove

        if self.dir == defined_direction['up']:
            self.y += self.speed * game_framework.frame_time
        elif self.dir == defined_direction['down']:
            self.y -= self.speed * game_framework.frame_time
        elif self.dir == defined_direction['right']:
            self.x += self.speed * game_framework.frame_time
        elif self.dir == defined_direction['left']:
            self.x -= self.speed * game_framework.frame_time

        self.x = clamp(50, self.x, width - 50)
        self.y = clamp(50, self.y, height - 50)

    def draw(self):
        ChuChu.images['move'][int(self.frame)].draw(self.x, self.y, 80, 105)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, other, group):
        if group == 'Link:ChuChu':
            if self.dir == defined_direction['up']:
                self.y -= 100
            elif self.dir == defined_direction['down']:
                self.y += 100
            elif self.dir == defined_direction['right']:
                self.x -= 100
            elif self.dir == defined_direction['left']:
                self.x += 100
        if group == 'Sword:ChuChu':
            game_world.remove_object(self, level['Monsters'])
        if group == 'Arrow:ChuChu':
            game_world.remove_object(self, level['Monsters'])
