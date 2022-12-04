from pico2d import *
import game_world
import game_framework

import server

from define_dir import up, down, right, left
from depth import level


class Arrow:
    image = None

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        if self.d == up or self.d == down:
            return sx - 12.5, sy - 37.5, sx + 12.5, sy + 37.5

        elif self.d == right or self.d == left:
            return sx - 37.5, sy - 12.5, sx + 37.5, sy + 12.5

    def handle_collision(self, other, group):
        if self in game_world.world[level['Objects']]:
            game_world.remove_object(self, level['Objects'])

    def __init__(self, x, y, velocity, d, ot):
        if Arrow.image is None:
            Arrow.image = load_image('Link/Item/arrow.png')
        self.x, self.y, self.velocity, self.d, self.ot = x, y, velocity, d, ot
        self.init_x, self.init_y = x, y

    def draw(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        draw_rectangle(*self.get_bb())
        if self.d == up:
            self.image.clip_draw(0, 0, 25, 75, sx, sy)

        elif self.d == down:
            self.image.clip_composite_draw(0, 0, 25, 75, 0, 'v', sx, sy, 25, 75)

        if self.d == right:
            self.image.clip_composite_draw(0, 0, 25, 75, -3.141592 / 2.0, '', sx, sy, 25, 75)

        elif self.d == left:
            self.image.clip_composite_draw(0, 0, 25, 75, 3.141592 / 2.0, '', sx, sy, 25, 75)

    def update(self):
        if self.ot < 0.4:
            game_world.remove_object(self, level['Objects'])

        if self.d == up:
            self.y += self.velocity * game_framework.frame_time

        elif self.d == down:
            self.y -= self.velocity * game_framework.frame_time

        if self.d == right:
            self.x += self.velocity * game_framework.frame_time

        elif self.d == left:
            self.x -= self.velocity * game_framework.frame_time

        if self.x < self.init_x - (self.velocity * self.ot) or self.x > self.init_x + (self.velocity * self.ot):
            game_world.remove_object(self, level['Objects'])

        if self.y < self.init_y - (self.velocity * self.ot) or self.y > self.init_y + (self.velocity * self.ot):
            game_world.remove_object(self, level['Objects'])
