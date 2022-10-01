from pico2d import *

running = True
width, height = 1440, 960

# direction is integer between 0 and 3
direction = 0
dir_x, dir_y = 0, 0
pos_x, pos_y = width // 2, height // 2

# run
    global dir_x, dir_y

# roll


# attack


open_canvas(width, height)


while running:
    clear_canvas()


    pos_x += dir_x * 10
    pos_y += dir_y * 10

    delay(0.05)


close_canvas()
