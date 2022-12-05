from pico2d import *
import random
import math

import game_framework
import game_world
import server

from sphere import Sphere

from define_dir import up, down, right, left
from define_PPM import Pixel_Per_Meter
from depth import level

from BehaviorTree import BehaviorTree, Leaf


class Eye:
    image = None
    hit_sound = None

    def __init__(self):
        if Eye.image is None:
            Eye.image = load_image('Monsters/Eye/eye.png')
        self.x = random.randint(50 + 192 + 1, server.bg.w - 50 - 192 - 1)
        self.y = server.bg.h - 50 - 192 - 1
        self.shoot_timer = 1.0
        self.font = load_font('Font/ENCR10B.TTF', 32)
        self.build_behavior_tree()
        if Eye.hit_sound is None:
            Eye.hit_sound = load_wav('Sound/Enemy/Enemy_Hit.wav')

    def update(self):
        self.bt.run()

        self.shoot_timer -= game_framework.frame_time

    def draw(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        Eye.image.draw(sx, sy, 50, 50)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        return sx - 25, sy - 25, sx + 25, sy + 25

    def handle_collision(self, other, group):
        if group == 'Sword:Monster':
            Eye.hit_sound.play()
            if self in game_world.world[level['Monsters']]:
                game_world.remove_object(self, level['Monsters'])
        if group == 'Arrow:Monster':
            Eye.hit_sound.play()
            if self in game_world.world[level['Monsters']]:
                game_world.remove_object(self, level['Monsters'])
        if group == 'Eye:Sphere':
            sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

            self.font.draw(sx, sy - 100, 'stunned!', (255, 255, 255))
            self.shoot_timer += 3.0

    # AI
    def shoot_sphere(self):
        if self.shoot_timer <= 0.0:
            self.shoot_timer = 1.0
            obj = Sphere(self.x, self.y - 25 - 45 - 1)
            game_world.add_object(obj, level['Objects'])
            game_world.add_collision_group(None, obj, 'Eye:Sphere')
            game_world.add_collision_group(None, obj, 'Link:Sphere')
            game_world.add_collision_group(obj, None, 'Sphere:Shield')

            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        shoot_node = Leaf('shoot sphere', self.shoot_sphere)

        self.bt = BehaviorTree(shoot_node)

