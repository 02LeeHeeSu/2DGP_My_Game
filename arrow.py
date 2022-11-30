from pico2d import *
import game_world
import game_framework

from define_dir import defined_direction
from depth import level


class Arrow:
    image = None

    def handle_event(self, event):
        pass

    def __init__(self, x, y, velocity, d, ot):
        if Arrow.image is None:
            Arrow.image = load_image('Link/Item/arrow.png')
        self.x, self.y, self.velocity, self.d, self.ot = x, y, velocity, d, ot
        self.init_x, self.init_y = x, y

    def draw(self):
        if self.d == defined_direction['up']:
            self.image.clip_draw(0, 0, 25, 75, self.x, self.y)

        elif self.d == defined_direction['down']:
            self.image.clip_composite_draw(0, 0, 25, 75, 0, 'v', self.x, self.y, 25, 75)

        if self.d == defined_direction['right']:
            self.image.clip_composite_draw(0, 0, 25, 75, -3.141592 / 2.0, '', self.x, self.y, 25, 75)

        elif self.d == defined_direction['left']:
            self.image.clip_composite_draw(0, 0, 25, 75, 3.141592 / 2.0, '', self.x, self.y, 25, 75)

    def update(self):
        if self.ot < 0.4:
            game_world.remove_object(self, level['Arrow'])

        if self.d == defined_direction['up']:
            self.y += self.velocity * game_framework.frame_time

        elif self.d == defined_direction['down']:
            self.y -= self.velocity * game_framework.frame_time

        if self.d == defined_direction['right']:
            self.x += self.velocity * game_framework.frame_time

        elif self.d == defined_direction['left']:
            self.x -= self.velocity * game_framework.frame_time

        if self.x < self.init_x - (self.velocity * self.ot) or self.x > self.init_x + (self.velocity * self.ot):
            game_world.remove_object(self)

        if self.y < self.init_y - (self.velocity * self.ot) or self.y > self.init_y + (self.velocity * self.ot):
            game_world.remove_object(self)
