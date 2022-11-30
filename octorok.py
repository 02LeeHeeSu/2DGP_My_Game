from pico2d import *
import game_framework
import game_world
import server

from define_dir import defined_direction
from define_PPM import Pixel_Per_Meter, Pixel_Per_Sec_octo
from depth import level


import random
from BehaviorTree import BehaviorTree, Selector, Sequence, Leaf

from canvas_size import width, height

PPS_rock = 4.0 * Pixel_Per_Sec_octo

Time_Per_Move = 1.0
Move_Per_Time = 1.0 / Time_Per_Move
FPMove = 2

Time_Per_Attack = 1.0
Attack_Per_Time = 1.0 / Time_Per_Attack
FPAttack = 2


def absolute(a):
    if a >= 0:
        return a
    else:
        return -a


animation_names = ['move', 'attack']


class Octorok:
    images = None

    def load_images(self):
        if Octorok.images is None:
            Octorok.images = {}
            for name in animation_names:
                Octorok.images[name] = [load_image("Monsters/Octorok/" + name + "%d" % i + "-" + "%d" % j + ".png") for i, j in [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)]]
    def get_bb(self):
        return self.x - 40, self.y - 45, self.x + 40, self.y + 45

    def __init__(self):
        self.hp = 1
        self.x, self.y = width - 80, height - 105
        self.load_images()
        self.dir = random.randint(0, 3)
        self.speed = 0
        self.timer = 1.0
        self.frame = 0
        self.build_behavior_tree()

    def wander(self):
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
        self.speed = Pixel_Per_Sec_octo
            self.dir = random.randint(0, 3)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def find_player(self):
        distance = (server.link.x - self.x) ** 2 + (server.link.y - self.y) ** 2
        if distance < (Pixel_Per_Meter * 10) ** 2:
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = 0.0

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

        return BehaviorTree.SUCCESS
                self.dir = defined_direction['down']

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
        Octorok.images['move'][int(self.frame) + self.dir * 2].draw(self.x, self.y, 80, 90)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, other, group):
        if group == 'Sword:Octorok':
            for obj in game_world.world[level['Octorok']]:
                if obj == self:
                    game_world.remove_object(self, level['Octorok'])
        if group == 'Arrow:Octorok':
            for obj in game_world.world[level['Octorok']]:
                if obj == self:
                    game_world.remove_object(self, level['Octorok'])
