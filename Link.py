from pico2d import *

running = True
width, height = 1080, 960

dir_x, dir_y = 0, 0
pos_x, pos_y = width // 2, height // 2

# run
def run_keydown(eventKey):
    global dir_x, dir_y



# roll


# attack


open_canvas(width, height)

run = load_image('Link/Run/right.png')
runFrame = 0

while running:
    clear_canvas()
    run.clip_draw(runFrame * 115, 0, 115, 120, pos_x, pos_y)
    update_canvas()

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
