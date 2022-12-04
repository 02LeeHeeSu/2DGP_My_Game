from pico2d import *

import game_world
import game_framework
import server

from depth import level

from background import Background

from link import MainCharacter
from slot import Slot
from heart import Heart

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


def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb:
        return False
    if ra < lb:
        return False
    if ta < bb:
        return False
    if ba > tb:
        return False

    return True


def enter():
    server.bg = Background()

    server.link = MainCharacter()
    server.HP = Heart()
    server.inventory = Slot()

    game_world.add_object(server.bg, level['Background'])

    game_world.add_object(server.link, level['Objects'])
    game_world.add_object(server.HP, level['UI'])
    game_world.add_object(server.inventory, level['UI'])

    game_world.add_collision_group(server.link, None, 'Link:Door')
    game_world.add_collision_group(server.link, None, 'Link:Rock')
    game_world.add_collision_group(server.link, None, 'Link:Monster')
    game_world.add_collision_group(server.link, None, 'Link:Item')

    game_world.add_collision_group(None, None, 'Sword:Monster')
    game_world.add_collision_group(None, None, 'Arrow:Monster')
    game_world.add_collision_group(None, None, 'Shield:Monster')

    game_world.add_collision_group(None, None, 'Rock:ChuChu')
    game_world.add_collision_group(None, None, 'Rock:Octorok')


def update():
    for obj in game_world.all_objects():
        obj.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print("collision by ", group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)


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
