from pico2d import *

import game_framework
import play_state

from canvas_size import width, height

image = None
sound = None


def enter():
    global image
    global sound

    image = load_image('Clear/game_clear.png')
    sound = load_music('Sound/Background/Game Clear.mp3')
    sound.set_volume(128)
    sound.play()


def exit():
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


def draw():
    clear_canvas()
    image.draw(width // 2, height // 2)
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
