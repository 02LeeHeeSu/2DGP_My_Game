from pico2d import *
import game_world
import server

from define_dir import up, down, right, left
from depth import level


class Sword:
    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom
        
        if server.link.Attack:
                return sx - 75, sy, sx + 75, sy + 112.5
                return sx - 75, sy - 112.5, sx + 75, sy
                return sx, sy - 100, sx + 115, sy + 100
                return sx - 115, sy - 100, sx, sy + 100
            if self.direction == up:
            elif self.direction == down:
            elif self.direction == right:
            elif self.direction == left:

        if server.link.Spin:
            return sx - 150, sy - 127.5 - 25, sx + 150, sy + 127.5 - 25

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
        pass

