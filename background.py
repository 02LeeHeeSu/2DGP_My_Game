from pico2d import *

from canvas_size import width, height

import server

from door import Door





class Background:
    def __init__(self):
        self.image = [[load_image('Background/background_%d%d.png' % (x, y)) for y in range(3)] for x in range(3)]
        self.x, self.y = stage_info.cur_room[0], stage_info.cur_room[1]
        self.w = self.image[self.x][self.y].w
        self.h = self.image[self.x][self.y].h

    def draw(self):
        self.image[self.x_index][self.y_index].clip_draw_to_origin(self.window_left, self.window_bottom,
                                                                   width, height,
                                                                   0, 0)

    def update(self):
        self.window_left = clamp(0, int(server.link.x) - width // 2, self.w - width - 1)
        self.window_bottom = clamp(0, int(server.link.y) - height // 2, self.h - height - 1)

    def handle_event(self, event):
        pass