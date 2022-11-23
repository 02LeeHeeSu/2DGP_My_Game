from pico2d import *

import game_world

import server

from link import MainCharacter
from slot import Slot
from heart import Heart
from chuchu import ChuChu
from octorok import Octorok

import game_framework

import pause_state


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.push_state(pause_state)
        else:
            for obj in game_world.all_objects():
                obj.handle_event(event)


def enter():
    server.link = MainCharacter()
    server.HP = Heart()
    server.inventory = Slot()

    server.chu = ChuChu()
    server.octo = Octorok()

    game_world.add_object(server.link, 1)
    game_world.add_object(server.HP, 1)
    game_world.add_object(server.inventory, 2)

    game_world.add_object(server.chu, 1)


def update():
    for obj in game_world.all_objects():
        obj.update()


def draw_world():
    for obj in game_world.all_objects():
        obj.draw()


def draw():
    clear_canvas()
    draw_world()
    update_canvas()


def exit():
    game_world.clear()


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
