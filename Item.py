from pico2d import *

ud, uu = range(2)

key_event_table = {
    (SDL_KEYDOWN, SDLK_u): ud,
    (SDL_KEYUP, SDLK_u): uu
}


class IDLE:
    @staticmethod
    def enter(self, event):
        pass

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        pass


class USE:
    @staticmethod
    def enter(self, event):
        pass

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        pass


next_state = {
    IDLE: {ud: USE, uu: IDLE},
    USE: {ud: USE, uu: IDLE}
}


# class Bow:
#     def __init__(self):
#         self.Use = False
#         self.Image_y_bow = load_image('Link/bow_down.png')
#         self.frame_y = 0
#         self.Image_y_arrow = load_image('Link/arrow_down.png')
#         self.arrow_x = 0
#         self.arrow_y = 0
#
#     def update(self):
#         if self.Use:
#             if self.frame_y < 9:
#                 self.frame_y += 1
#         elif not self.Use and self.frame_y >= 9:
#             self.frame_y = (self.frame_y + 1) % 13
#
#     def draw(self):
#         if self.Use:
#             clear_canvas()
#             self.Image_y_bow.clip_draw(self.frame_y * 140, 0, 140, 130, Link.x, Link.y)
#         elif not self.Use and self.frame_y != 0:
#             self.Image_y_arrow.draw(Link.x, Link.y)
