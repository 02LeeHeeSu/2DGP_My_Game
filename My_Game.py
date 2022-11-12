import game_framework
import pico2d
import logo_state

from canvas_size import width, height

pico2d.open_canvas(width, height)
game_framework.run(logo_state)
pico2d.close_canvas()
