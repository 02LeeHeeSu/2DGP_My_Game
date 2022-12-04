from pico2d import *

from canvas_size import width, height

import server

from door import Door





class Background:
    def __init__(self):
        self.image = [[load_image('Background/background_%d%d.png' % (x, y)) for y in range(3)] for x in range(3)]
        self.x_index, self.y_index = x_index['center'], y_index['top']
        self.w = self.image[self.x_index][self.y_index].w
        self.h = self.image[self.x_index][self.y_index].h
        self.cur_room = room_info[self.x_index][self.y_index]

    def draw(self):
        self.image[self.x_index][self.y_index].clip_draw_to_origin(self.window_left, self.window_bottom,
                                                                   width, height,
                                                                   0, 0)

    def update(self):
        self.window_left = clamp(0, int(server.link.x) - width // 2, self.w - width - 1)
        self.window_bottom = clamp(0, int(server.link.y) - height // 2, self.h - height - 1)

    def handle_event(self, event):
        pass