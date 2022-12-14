from pico2d import *

import server

from define_dir import up, down, right, left


class Shield:
    def __init__(self, x, y, d):
        self.x, self.y, self.d = x, y, d
        self.sound = load_wav('Sound/Objects/Shield_Deflect.wav')

    def update(self):
        self.x, self.y = server.link.x, server.link.y

    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom
        
        if self.d == up:
            return sx - 45, sy + 35 - 25, sx + 45, sy + 35 + 25
        elif self.d == down:
            return sx - 45, sy - 35 - 25, sx + 45, sy - 35 + 25
        elif self.d == right:
            return sx + 45 - 12.5, sy - 55, sx + 45 + 12.5, sy + 55
        elif self.d == left:
            return sx - 45 - 12.5, sy - 55, sx - 45 + 12.5, sy + 55

    def handle_collision(self, other, group):
        self.sound.play()
