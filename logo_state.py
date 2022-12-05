from pico2d import *

import game_framework
import title_state

from canvas_size import width, height

image = None
logo_time = 0.0


def enter():
    global image, logo_time
    image = load_image('Credit/tuk_credit.png')
    logo_time = 0.0


def exit():
    global image
    del image


def update():
    global logo_time

    logo_time += game_framework.frame_time

    if logo_time > 1.0:
        game_framework.change_state(title_state)


def draw():
    global image

    clear_canvas()
    image.draw(width // 2, height // 2)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()


def test_self():
    import sys
    open_canvas(1440, 960)
    game_framework.run(sys.modules['__main__'])
    close_canvas()


if __name__ == '__main__':
    test_self()
