from pico2d import *

import game_framework
import title_state

image = None
logo_time = 0.0


def enter():
    global image, logo_time
    image = load_image('Credit/tuk_credit.png')
    logo_time = 0.0


def end():
    global image
    del image


def update():
    global logo_time

    delay(0.05)
    logo_time += 0.05

    if logo_time > 1.0:
        game_framework.change_state(title_state)


def draw():
    global image

    clear_canvas()
    image.draw(720, 480)
    update_canvas()


def handle_events():
    events = get_events()


def test_self():
    import sys
    open_canvas(1440, 960)
    game_framework.run(sys.modules['__main__'])
    close_canvas()


if __name__ == '__main__':
    test_self()
