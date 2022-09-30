from pico2d import *

running = True
width, height = 1080, 960

dir_x, dir_y = 0, 0
pos_x, pos_y = width // 2, height // 2

# run
def run_link():
    global running
    global dir_x, dir_y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False


# roll


# attack


open_canvas(width, height)


while running:
    clear_canvas()
    update_canvas()
    run_link()
    delay(0.05)


close_canvas()
