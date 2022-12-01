from pico2d import *
import game_framework
import game_world
import server

from define_dir import defined_direction
from define_PPM import Pixel_Per_Meter, Pixel_Per_Sec_octo
from depth import level

from rock import Rock

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
                Octorok.images[name] = [load_image("Monsters/Octorok/" + name + "%d" % i + "-" + "%d" % j + ".png") for
                                        i, j in [(0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2)]]

    def get_bb(self):
        return self.x - 40, self.y - 45, self.x + 40, self.y + 45

    def __init__(self):
        self.x, self.y = width - 80, height - 90
        self.load_images()
        self.dir = random.randint(0, 3)
        self.speed = 0
        self.wander_timer = 1.0
        self.Attack = False
        self.attack_distance = (Pixel_Per_Meter * 10) ** 2
        self.attack_timer = 1.0
        self.is_shoot = False
        self.frame_move = 0
        self.frame_attack = 0
        self.build_behavior_tree()

    def wander(self):
        self.Attack = False
        self.speed = Pixel_Per_Sec_octo
        self.wander_timer -= game_framework.frame_time
        if self.wander_timer <= 0:
            self.wander_timer = 1.0
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

    def look_and_attack_player(self):
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
                self.dir = defined_direction['down']

        x = absolute(server.link.x - self.x) ** 2
        y = absolute(server.link.y - self.y) ** 2
        distance = x + y

        if distance < self.attack_distance:
            if self.dir == defined_direction['up'] and self.x - 40 < x < self.x + 40:
                self.Attack = True
                return BehaviorTree.SUCCESS
            elif self.dir == defined_direction['down'] and self.x - 40 < x < self.x + 40:
                self.Attack = True
                return BehaviorTree.SUCCESS
            elif self.dir == defined_direction['right'] and self.y - 45 < y < self.y + 45:
                self.Attack = True
                return BehaviorTree.SUCCESS
            elif self.dir == defined_direction['left'] and self.y - 45 < y < self.y + 45:
                self.Attack = True
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wander_node = Leaf("Wander", self.wander)
        find_player_node = Leaf("Find Player", self.find_player)
        look_at_player_node = Leaf("Look and attack Player", self.look_and_attack_player)
        chase_node = Sequence("Chase")
        chase_node.add_children(find_player_node, look_at_player_node)
        wander_chase_node = Selector("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)

    def shoot_rock(self):
        if self.dir == defined_direction['up']:
            threw_rock = Rock(self.x, self.y + 45 + 20 + 1, PPS_rock, self.dir, self.attack_distance)
            game_world.add_object(threw_rock, 1)
            game_world.add_collision_group(threw_rock, None, 'Rock:Link')
            game_world.add_collision_group(threw_rock, None, 'Rock:Shield')

        elif self.dir == defined_direction['down']:
            threw_rock = Rock(self.x, self.y - 45 - 20 - 1, PPS_rock, self.dir, self.attack_distance)
            game_world.add_object(threw_rock, 1)
            game_world.add_collision_group(threw_rock, None, 'Rock:Link')
            game_world.add_collision_group(threw_rock, None, 'Rock:Shield')

        elif self.dir == defined_direction['right']:
            threw_rock = Rock(self.x + 40 + 20 + 1, self.y, PPS_rock, self.dir, self.attack_distance)
            game_world.add_object(threw_rock, 1)
            game_world.add_collision_group(threw_rock, None, 'Rock:Link')
            game_world.add_collision_group(threw_rock, None, 'Rock:Shield')

        elif self.dir == defined_direction['left']:
            threw_rock = Rock(self.x - 40 - 20 - 1, self.y, PPS_rock, self.dir, self.attack_distance)
            game_world.add_object(threw_rock, 1)
            game_world.add_collision_group(threw_rock, None, 'Rock:Link')
            game_world.add_collision_group(threw_rock, None, 'Rock:Shield')

    def update(self):
        self.bt.run()

        self.frame_move = (self.frame_move + FPMove * Move_Per_Time * game_framework.frame_time) % FPMove

        if self.Attack:
            self.frame_attack = (self.frame_attack + FPAttack * Attack_Per_Time * game_framework.frame_time) % FPAttack
            self.attack_timer -= game_framework.frame_time

            if self.attack_timer <= 0.0:
                self.attack_timer = 1.0
                self.is_shoot = False

        if int(self.frame_attack) == 1 and not self.is_shoot:
            self.is_shoot = True
            self.shoot_rock()

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
        if self.Attack:
            Octorok.images['attack'][int(self.frame_move) + self.dir * 2].draw(self.x, self.y, 80, 90)
        else:
            Octorok.images['move'][int(self.frame_move) + self.dir * 2].draw(self.x, self.y, 80, 90)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, other, group):
        if group == 'Sword:Octorok':
            game_world.remove_object(self, level['Monsters'])
        if group == 'Arrow:Octorok':
            game_world.remove_object(self, level['Monsters'])
        if group == 'Rock:Octorok':
            game_world.remove_object(self, level['Monsters'])
