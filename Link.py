from pico2d import *

running = True
width, height = 1440, 960

# direction is integer between 0 and 3
direction = 0
dir_x, dir_y = 0, 0
pos_x, pos_y = width // 2, height // 2

# run
def run_link():
    global running
    global direction
    global dir_x, dir_y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_w:
                direction = 0
                dir_y += 1
            elif event.key == SDLK_s:
                direction = 1
                dir_y -= 1
            elif event.key == SDLK_d:
                direction = 2
                dir_x += 1
            elif event.key == SDLK_a:
                direction = 3
                dir_x -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w:
                dir_y -= 1
            elif event.key == SDLK_s:
                dir_y += 1
            elif event.key == SDLK_d:
                dir_x -= 1
            elif event.key == SDLK_a:
                dir_x += 1
# roll


# attack


open_canvas(width, height)


while running:
    clear_canvas()


    pos_x += dir_x * 10
    pos_y += dir_y * 10

    delay(0.05)


close_canvas()
