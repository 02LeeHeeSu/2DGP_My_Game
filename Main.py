from pico2d import *

running = True
width, height = 1440, 960
dir_x, dir_y = 0, 0


def dir_to_frame(direction):
    if direction < 2:
        return -direction + 1
    else:
        return -direction + 3


def run_kd(key):
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

    if key == SDLK_w:
        dir_y -= 1
    elif key == SDLK_s:
        dir_y += 1
    elif key == SDLK_d:
        dir_x -= 1
    elif key == SDLK_a:
        dir_x += 1


# 주인공 객체 생성
class MainCharacter:
    def __init__(self):
        self.x, self.y = width // 2, height // 2   # 위치

        self.direction = 1  # 방향

        self.Stand = load_image('Link/Stand/Stand.png') # 서 있는 상태

        self.Run = False
        self.Run_x = load_image('Link/Run/run_x.png')   # 달리기
        self.Run_y = load_image('Link/Run/run_y.png')
        self.Run_frame_x, self.Run_frame_y = 0, 0

        self.Roll = False
        self.Roll_x = load_image('Link/Roll/roll_x.png')    # 구르기
        self.Roll_y = load_image('Link/Roll/roll_y.png')
        self.Roll_frame_x, self.Roll_frame_y = 0, 0

        self.Attack = False
        self.Attack_x = load_image('Link/Attack/attack_x.png')  # 공격
        self.Attack_y = load_image('Link/Attack/attack_y.png')
        self.Attack_frame_x, self.Attack_frame_y = 0, 0

    def update(self):
    def draw(self):
# 적 객체 생성


# 초기화
open_canvas(width, height)
# 게임 루프
while running:
    clear_canvas()

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
    update_canvas()


    delay(0.05)

close_canvas()
