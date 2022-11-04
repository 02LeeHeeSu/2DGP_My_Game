from pico2d import *
from Link import MainCharacter
from slot import Slot

import game_framework
import pause_state

width, height = 1440, 960


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()


class Bow:
    def __init__(self):
        self.Use = False
# 게임 초기화: 객체 생성
Link = None
slot = None
bow = None


def enter():
    global Link, slot, bow
    Link = MainCharacter()
    slot = Slot()
    bow = Bow()


def update():
    Link.update()
    delay(0.04)


def draw_world():
    Link.draw()
    slot.draw()


def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def exit():
    global Link, slot
    del Link
    del slot


def pause():
    pass


def resume():
    pass


# def test_self():
#     import sys
#     open_canvas(width, height)
#     game_framework.run(sys.modules['__main__'])
#     close_canvas()
#
#
# if __name__ == '__main__':
#     test_self()
