from pico2d import *
import game_world
import game_framework

width, height = 1440, 960


class Arrow:
    image = None

    def handle_event(self, event):
        pass

    def __init__(self, x, y, velocity, d, ot):
        if Arrow.image is None:
            Arrow.image = load_image('Link/Item/arrow.png')
        self.x, self.y, self.velocity, self.d, self.ot = x, y, velocity, d, ot

    def draw(self):
        if self.d == 0:
            self.image.clip_draw(0, 0, 25, 75, self.x, self.y)

        elif self.d == 1:
            self.image.clip_composite_draw(0, 0, 25, 75, 0, 'v', self.x, self.y, 25, 75)

        if self.d == 2:
            self.image.clip_composite_draw(0, 0, 25, 75, -3.141592 / 2.0, '', self.x, self.y, 25, 75)

        elif self.d == 3:
            self.image.clip_composite_draw(0, 0, 25, 75, 3.141592 / 2.0, '', self.x, self.y, 25, 75)

    def update(self):
        if self.d == 0:
            self.y += self.velocity * game_framework.frame_time

        elif self.d == 1:
            self.y -= self.velocity * game_framework.frame_time

        if self.d == 2:
            self.x += self.velocity * game_framework.frame_time

        elif self.d == 3:
            self.x -= self.velocity * game_framework.frame_time

        if (self.x < 45 or self.x > width - 45) or (self.y < 60 or self.y > width - 60):
            game_world.remove_object(self)
