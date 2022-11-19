import random
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *

import server

from canvas_size import width, height

Pixel_Per_Meter = (10.0 / 0.15)
KM_Per_Hour = 10.0
Meter_Per_Minute = (KM_Per_Hour * 1000.0 / 60.0)
Meter_Per_Sec = (Meter_Per_Minute / 60.0)
Pixel_Per_Sec = (Meter_Per_Sec * Pixel_Per_Meter)

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

    def __init__(self):
        self.x, self.y = 80, 105
        self.load_images()
        self.dir = random.randint(0, 3)
        self.speed = 0
        self.timer = 1.0
        self.frame = 0
        self.build_behavior_tree()

    def wander(self):
        self.speed = Pixel_Per_Sec
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
            self.dir = random.randint(0, 3)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def find_player(self):
        distance = (server.Link.x - self.x) ** 2 + (server.Link.y - self.y) ** 2
        if distance < (Pixel_Per_Meter * 10) ** 2:
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = Pixel_Per_Sec

        dx = server.Link.x - self.x
        dy = server.Link.y - self.y

        if dx >= 0 and dy >= 0:
            if dx >= dy:
                self.dir = 2
            else:
                self.dir = 0

        if dx >= 0 > dy:
            dy = absolute(dy)

            if dx >= dy:
                self.dir = 2
            else:
                self.dir = 1

        if dx < 0 <= dy:
            dx = absolute(dx)

            if dx >= dy:
                self.dir = 3
            else:
                self.dir = 0

        if dx < 0 and dy < 0:
            dx = absolute(dx)
            dy = absolute(dy)

            if dx >= dy:
                self.dir = 3
            else:
                self.dir = 1

        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)

    def update(self):
        self.bt.run()

        self.frame = (self.frame + FPMove * Move_Per_Time * game_framework.frame_time) % FPMove

        if self.dir == 0:
            self.y += self.speed * game_framework.frame_time
        elif self.dir == 1:
            self.y -= self.speed * game_framework.frame_time
        elif self.dir == 2:
            self.x += self.speed * game_framework.frame_time
        elif self.dir == 3:
            self.x -= self.speed * game_framework.frame_time

        self.x = clamp(50, self.x, width - 50)
        self.y = clamp(50, self.y, height - 50)

    def draw(self):
        ChuChu.images['move'][int(self.frame)].draw(self.x, self.y, 80, 105)

    def handle_event(self, event):
        pass
