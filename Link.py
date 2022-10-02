from pico2d import *

running = True
width, height = 1440, 960

# direction is integer between 0 and 3
direction = 1
dir_x, dir_y = 0, 0
pos_x, pos_y = width // 2, height // 2

Run = False
Roll = False
roll_repeat = 0


# run
def run_kd(key):
    global direction
    global dir_x, dir_y

    if key == SDLK_w:
        dir_y += 1
    elif key == SDLK_s:
        dir_y -= 1
    elif key == SDLK_d:
        dir_x += 1
    elif key == SDLK_a:
        dir_x -= 1


def run_ku(key):
    global dir_x, dir_y
    global Run

    if key == SDLK_w:
        dir_y -= 1
    elif key == SDLK_s:
        dir_y += 1
    elif key == SDLK_d:
        dir_x -= 1
    elif key == SDLK_a:
        dir_x += 1


# attack


open_canvas(width, height)

stand = load_image('Link/Stand/Stand.png')

run_x = load_image('Link/Run/run_x.png')
run_x_Frame_w = 0
run_x_Frame_h = 1
run_y = load_image('Link/Run/run_y.png')
run_y_Frame_w = 0
run_y_Frame_h = 0

roll_x = load_image('Link/Roll/roll_x.png')
roll_x_Frame_w = 0
roll_x_Frame_h = 1
roll_y = load_image('Link/Roll/roll_y.png')
roll_y_Frame_w = 0
roll_y_Frame_h = 0

while running:
    if dir_x == 0 and dir_y == 0:
        Run = False

    else:
        Run = True
        if dir_y > 0:
            direction = 0
        elif dir_y < 0:
            direction = 1
        if dir_x > 0:
            direction = 2
        elif dir_x < 0:
            direction = 3

    clear_canvas()

    # 서 있는 상태 확인
    if not Run and not Roll:
        stand.clip_draw(direction * 90, 0, 90, 120, pos_x, pos_y)

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_w or event.key == SDLK_s or event.key == SDLK_d or event.key == SDLK_a:
                run_kd(event.key)
            elif event.key == SDLK_l:
                Roll = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w or event.key == SDLK_s or event.key == SDLK_d or event.key == SDLK_a:
                run_ku(event.key)
            elif event.key == SDLK_l:
                pass

    if (direction == 0 or direction == 1) and Run:
        run_y.clip_draw(run_y_Frame_w * 90, run_y_Frame_h * 120, 90, 120, pos_x, pos_y)
        run_y_Frame_w = (run_y_Frame_w + 1) % 10
        if direction == 0:
            run_y_Frame_h = 1
        else:
            run_y_Frame_h = 0
    elif (direction == 2 or direction == 3) and Run:
        run_x.clip_draw(run_x_Frame_w * 115, run_x_Frame_h * 120, 115, 120, pos_x, pos_y)
        run_x_Frame_w = (run_x_Frame_w + 1) % 10
        if direction == 2:
            run_x_Frame_h = 1
        else:
            run_x_Frame_h = 0

    update_canvas()

    if pos_x < 45:
        pos_x = 45
    elif pos_x > width - 45:
        pos_x = width - 45

    if pos_y < 60:
        pos_y = 60
    elif pos_y > height - 60:
        pos_y = height - 60

    pos_x += dir_x * 10
    pos_y += dir_y * 10
    if Roll:
        roll_repeat += 1

    if roll_repeat == 9:
        roll_repeat = 0
        Roll = False

    delay(0.05)

close_canvas()
