from pico2d import *
import game_world
import game_framework

import server

from define_PPM import Pixel_Per_Meter, Pixel_Per_Sec_sphere
from depth import level

Time_Per_Update = 0.5
Update_Per_Time = 1.0 / Time_Per_Update
FPUpdate = 5


class Sphere:
    images = None
    shoot_sound = None

    def __init__(self, x, y):
        if Sphere.images is None:
            Sphere.images = [load_image('Monsters/Eye/' + 'sphere' + '%d' % i + '.png') for i in range(1, 5 + 1)]
        self.x, self.y = x, y
        self.init_x, self.init_y = x, y
        self.velocity = Pixel_Per_Sec_sphere
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FPUpdate * Update_Per_Time * game_framework.frame_time) % FPUpdate

        self.y -= self.velocity * game_framework.frame_time

        if self.y < self.init_y - Pixel_Per_Meter * 20:
            game_world.remove_object(self, level['Objects'])

    def draw(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom
        Sphere.images[int(self.frame)].clip_composite_draw(0, 0, 15, 15, 0, '', sx, sy, 45, 45)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        return sx - 22.5, sy - 22.5, sx + 22.5, sy + 22.5

    def handle_collision(self, other, group):
        if group == 'Link:Sphere':
            game_world.remove_object(self, level['Objects'])
        if group == 'Sphere:Shield':
            self.velocity *= -1
        if group == 'Eye:Sphere':
            game_world.remove_object(self, level['Objects'])
