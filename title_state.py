from pico2d import *

import game_framework
import play_state

image = None


def enter():
    global image

    image = load_image('Title/title.png')


def end():
    global image
    del image


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_SPACE:
                game_framework.change_state(play_state)


def draw():
    clear_canvas()
    image.draw(720, 480)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass


def test_self():
    import sys
    open_canvas(1440, 960)
    game_framework.run(sys.modules['__main__'])
    close_canvas()


if __name__ == '__main__':
    test_self()
