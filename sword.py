from pico2d import *

import game_world
import server

from vaati import Vaati

from define_dir import up, down, right, left
from depth import level


class Sword:
    def __init__(self, direction):
        self.x, self.y = server.link.x, server.link.y
        self.direction = direction

    def update(self):
        self.x, self.y = server.link.x, server.link.y

    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        if server.link.Attack:
            if self.direction == up:
                return sx - 75, sy, sx + 75, sy + 150
            elif self.direction == down:
                return sx - 75, sy - 150, sx + 75, sy
            elif self.direction == right:
                return sx, sy - 75, sx + 150, sy + 75
            elif self.direction == left:
                return sx - 150, sy - 75, sx, sy + 75

        if server.link.Spin:
            return sx - 150, sy - 127.5 - 25, sx + 150, sy + 127.5 - 25

    def handle_collision(self, other, group):
        if group == 'Sword:Monster':
            if type(other) is Vaati and other.is_stopped:
                if self in game_world.world[level['Objects']]:
                    game_world.remove_object(self, level['Objects'])

