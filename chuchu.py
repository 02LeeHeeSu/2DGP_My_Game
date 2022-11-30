from pico2d import *
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
        self.load_images()
        self.dir = random.randint(0, 3)
        self.speed = 0
        self.timer = 1.0
        self.frame = 0
        self.build_behavior_tree()

    def wander(self):
        self.speed = Pixel_Per_Sec_chu
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
            self.dir = random.randint(0, 3)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def find_player(self):
        distance = (server.link.x - self.x) ** 2 + (server.link.y - self.y) ** 2
        if distance < (Pixel_Per_Meter * 5) ** 2:
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = Pixel_Per_Sec_chu

        dx = server.link.x - self.x
        dy = server.link.y - self.y

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

        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        wander_node = Leaf("Wander", self.wander)
        find_player_node = Leaf("Find Player", self.find_player)
        move_to_player_node = Leaf("Move to Player", self.move_to_player)
        chase_node = Sequence("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        wander_chase_node = Selector("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)

    def update(self):
        self.bt.run()

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
            for obj in game_world.world[level['ChuChu']]:
                if obj == self:
                    game_world.remove_object(self, level['ChuChu'])
        if group == 'Arrow:ChuChu':
            for obj in game_world.world[level['ChuChu']]:
                if obj == self:
                    game_world.remove_object(self, level['ChuChu'])
