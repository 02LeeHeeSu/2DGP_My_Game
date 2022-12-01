from pico2d import *
import game_world
import game_framework

import server

from define_dir import defined_direction
from depth import level

Time_Per_Attack = 1.0
Attack_Per_Time = 1.0 / Time_Per_Attack
FPAttack = 3


class Rock:
    image = None

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        return sx - 20, sy - 20, sx + 20, sy + 20

    def handle_collision(self, other, group):
        if group == 'Rock:Link':
            if self in game_world.world[level['Objects']]:
                game_world.remove_object(self, level['Objects'])

        if group == 'Rock:Shield':
            if self.direction == defined_direction['up']:
                self.direction = defined_direction['down']

            elif self.direction == defined_direction['down']:
                self.direction = defined_direction['up']

            elif self.direction == defined_direction['right']:
                self.direction = defined_direction['left']

            elif self.direction == defined_direction['left']:
                self.direction = defined_direction['right']

        if group == 'Rock:Octorok':
            game_world.remove_object(self, level['Objects'])

    def __init__(self, x, y, velocity, direction, distance):
        if Rock.image is None:
            Rock.image = load_image('Monsters/Octorok/rock.png')
        self.x, self.y, self.velocity, self.direction, self.distance = x, y, velocity, direction, distance
        self.init_x, self.init_y = x, y
        self.frame = 0

    def draw(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom
        self.image.clip_draw(int(self.frame) * 40, 0, 40, 40, sx, sy)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + FPAttack * Attack_Per_Time * game_framework.frame_time) % FPAttack

        if self.direction == defined_direction['up']:
            self.y += self.velocity * game_framework.frame_time

        elif self.direction == defined_direction['down']:
            self.y -= self.velocity * game_framework.frame_time

        if self.direction == defined_direction['right']:
            self.x += self.velocity * game_framework.frame_time

        elif self.direction == defined_direction['left']:
            self.x -= self.velocity * game_framework.frame_time

        if self.x < self.init_x - self.distance or self.x > self.init_x + self.distance:
            game_world.remove_object(self, level['Objects'])

        if self.y < self.init_y - self.distance or self.y > self.init_y + self.distance:
            game_world.remove_object(self, level['Objects'])
