from pico2d import *
import random
import math

import game_framework
import game_world
import server

from define_dir import up, down, right, left
from define_PPM import Pixel_Per_Meter, Pixel_Per_Sec_octo
from depth import level

from rock import Rock

from BehaviorTree import BehaviorTree, Leaf

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


def calculate_distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


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
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        return sx - 40, sy - 45, sx + 40, sy + 45

    def __init__(self):
        self.x = random.randint(40 + 192 + 45 + 1, server.bg.w - 40 - 192 - 45 - 1)
        self.y = random.randint(45 + 192 + 60 + 1, server.bg.h - 45 - 192 - 60 - 1)
        self.load_images()
        self.dir = random.randint(up, left)
        self.speed = 0
        self.wander_timer = 1.0
        self.Attack = False
        self.attack_distance = Pixel_Per_Meter * 10
        self.attack_timer = Time_Per_Attack
        self.frame_move = 0
        self.frame_attack = 0
        self.build_behavior_tree()

    def look_player(self):
        dx = server.link.x - self.x
        dy = server.link.y - self.y

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

    def look_random(self):
        dx = random.randint(40, width - 40) - self.x
        dy = random.randint(45, height - 45) - self.y

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

    def check_attack_distance_is_in_range(self):
        distance = calculate_distance(server.link, self)

        if distance > self.attack_distance:
            if self.wander_timer <= 0.0:
                self.look_random()
            self.speed = Pixel_Per_Sec_octo
            self.Attack = False

        self.look_player()

        if distance <= self.attack_distance:
            if self.dir == up or self.dir == down:
                if self.x - 45 <= server.link.x <= self.x + 45:
                    self.speed = 0
                    self.Attack = True
                    return BehaviorTree.SUCCESS
                else:
                    return BehaviorTree.FAIL

            if self.dir == right or self.dir == left:
                if self.y - 60 <= server.link.y <= self.y + 60:
                    self.speed = 0
                    self.Attack = True
                    return BehaviorTree.SUCCESS
                else:
                    return BehaviorTree.FAIL

    def build_behavior_tree(self):
        check_node = Leaf('Check attack distance is in range', self.check_attack_distance_is_in_range)

        self.bt = BehaviorTree(check_node)

    def shoot_rock(self):
        if self.dir == up:
            threw_rock = Rock(self.x, self.y + 45 + 20 + 1, PPS_rock, self.dir, self.attack_distance)
            game_world.add_object(threw_rock, level['Objects'])
            game_world.add_collision_group(threw_rock, None, 'Rock:Link')
            game_world.add_collision_group(threw_rock, None, 'Rock:Shield')
            game_world.add_collision_group(threw_rock, None, 'Rock:Octorok')

        elif self.dir == down:
            threw_rock = Rock(self.x, self.y - 45 - 20 - 1, PPS_rock, self.dir, self.attack_distance)
            game_world.add_object(threw_rock, level['Objects'])
            game_world.add_collision_group(threw_rock, None, 'Rock:Link')
            game_world.add_collision_group(threw_rock, None, 'Rock:Shield')
            game_world.add_collision_group(threw_rock, None, 'Rock:Octorok')

        elif self.dir == right:
            threw_rock = Rock(self.x + 40 + 20 + 1, self.y, PPS_rock, self.dir, self.attack_distance)
            game_world.add_object(threw_rock, level['Objects'])
            game_world.add_collision_group(threw_rock, None, 'Rock:Link')
            game_world.add_collision_group(threw_rock, None, 'Rock:Shield')
            game_world.add_collision_group(threw_rock, None, 'Rock:Octorok')

        elif self.dir == left:
            threw_rock = Rock(self.x - 40 - 20 - 1, self.y, PPS_rock, self.dir, self.attack_distance)
            game_world.add_object(threw_rock, level['Objects'])
            game_world.add_collision_group(threw_rock, None, 'Rock:Link')
            game_world.add_collision_group(threw_rock, None, 'Rock:Shield')
            game_world.add_collision_group(threw_rock, None, 'Rock:Octorok')

    def update(self):
        self.bt.run()

        self.wander_timer -= game_framework.frame_time

        self.frame_move = (self.frame_move + FPMove * Move_Per_Time * game_framework.frame_time) % FPMove

        if self.Attack:
            self.frame_attack = (self.frame_attack + FPAttack * Attack_Per_Time * game_framework.frame_time) % FPAttack
            self.attack_timer -= game_framework.frame_time
            if self.attack_timer <= 0.0:
                self.shoot_rock()
                self.attack_timer = Time_Per_Attack
        else:
            self.attack_timer = Time_Per_Attack
            self.frame_attack = 0

        if self.dir == up:
            self.y += self.speed * game_framework.frame_time
        elif self.dir == down:
            self.y -= self.speed * game_framework.frame_time
        elif self.dir == right:
            self.x += self.speed * game_framework.frame_time
        elif self.dir == left:
            self.x -= self.speed * game_framework.frame_time

        self.x = clamp(50, self.x, width - 50)
        self.y = clamp(50, self.y, height - 50)

    def draw(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        if self.Attack:
            Octorok.images['attack'][int(self.frame_move) + self.dir * 2].draw(sx, sy, 80, 90)
        else:
            Octorok.images['move'][int(self.frame_move) + self.dir * 2].draw(sx, sy, 80, 90)
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
