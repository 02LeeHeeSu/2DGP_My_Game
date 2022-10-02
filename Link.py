from pico2d import *

running = True
width, height = 1440, 960

# direction is integer between 0 and 3
direction = 1
dir_x, dir_y = 0, 0
pos_x, pos_y = width // 2, height // 2

Run = False


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


# roll


# attack


open_canvas(width, height)

run_x = load_image('Link/Run/run_x.png')
run_x_Frame_w = 0
run_x_Frame_h = 1
run_y = load_image('Link/Run/run_y.png')
run_y_Frame_w = 0
run_y_Frame_h = 0

while running:
    clear_canvas()


    pos_x += dir_x * 10
    pos_y += dir_y * 10

    if direction == 0 or direction == 1:
        run_y.clip_draw(run_y_Frame_w * 90, run_y_Frame_h * 120, 90, 120, pos_x, pos_y)
        run_y_Frame_w = (run_y_Frame_w + 1) % 10
        if direction == 0:
            run_y_Frame_h = 1
        else:
            run_y_Frame_h = 0
    elif direction == 2 or direction == 3:
        run_x.clip_draw(run_x_Frame_w * 115, run_x_Frame_h * 120, 115, 120, pos_x, pos_y)
        run_x_Frame_w = (run_x_Frame_w + 1) % 10
        if direction == 2:
            run_x_Frame_h = 1
        else:
            run_x_Frame_h = 0

    update_canvas()

    delay(0.05)


close_canvas()
