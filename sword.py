from pico2d import *
import game_world
import server

from define_dir import defined_direction
from depth import level


class Sword:
    def get_bb(self):
        if server.link.Attack:
            if self.direction == defined_direction['up']:
                return self.x - 75, self.y, self.x + 75, self.y + 112.5
            elif self.direction == defined_direction['down']:
                return self.x - 75, self.y - 112.5, self.x + 75, self.y
            elif self.direction == defined_direction['right']:
                return self.x, self.y - 100, self.x + 115, self.y + 100
            elif self.direction == defined_direction['left']:
                return self.x - 115, self.y - 100, self.x, self.y + 100

        if server.link.Spin:
            return self.x - 150, self.y - 127.5 - 25, self.x + 150, self.y + 127.5 - 25

        else:
            return 0, 0, 0, 0

    def __init__(self, direction):
        self.x, self.y = server.link.x, server.link.y
        self.direction = direction

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, other, group):
        game_world.remove_object(self, level['Sword'])

