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
            elif event.key == SDLK_w:
                dir_y += 1
            elif event.key == SDLK_s:
                dir_y -= 1
            elif event.key == SDLK_d:
                dir_x += 1
            elif event.key == SDLK_a:
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

run = load_image('Link/Run/right.png')
runFrame = 0

while running:
    clear_canvas()
    run.clip_draw(runFrame * 115, 0, 115, 120, pos_x, pos_y)
    update_canvas()

    run_link()
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            run_keydown(event.key)
        elif event.type == SDL_KEYUP:
            run_keyup(event.key)

    pos_x += dir_x * 10
    pos_y += dir_y * 10

    runFrame = (runFrame + 1) % 10
    delay(0.05)


close_canvas()
