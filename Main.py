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
        if self.Run and not(self.Roll or self.Attack):
            self.x += dir_x * 10
            self.y += dir_y * 10

            self.Run_frame_x = (self.Run_frame_x + 1) % 10
            self.Run_frame_y = (self.Run_frame_y + 1) % 10

        if self.Roll:
            if self.direction == 0 or self.direction == 1:
                if self.direction == 0:
                    self.y += 20
                else:
                    self.y -= 20

                self.Roll_frame_y = (self.Roll_frame_y + 1) % 9
                if self.Roll_frame_y == 0:
                    self.Roll = False
            elif self.direction == 2 or self.direction == 3:
                if self.direction == 2:
                    self.x += 18
                else:
                    self.x -= 18

                self.Roll_frame_x = (self.Roll_frame_x + 1) % 10
                if self.Roll_frame_x == 0:
                    self.Roll = False

        if self.Attack:
            if self.direction == 0 or self.direction == 1:
                self.Attack_frame_y = (self.Attack_frame_y + 1) % 7
                if self.Attack_frame_y == 0:
                    self.Attack = False
            elif self.direction == 2 or self.direction == 3:
                self.Attack_frame_x = (self.Attack_frame_x + 1) % 7
                if self.Attack_frame_x == 0:
                    self.Attack = False

        if self.x < 45:
            self.x = 45
        elif self.x > width - 45:
            self.x = width - 45

        if self.y < 60:
            self.y = 60
        elif self.y > height - 60:
            self.y = height - 60

    def draw(self):
        if not (self.Run or self.Roll or self.Attack):
            self.Stand.clip_draw(self.direction * 90, 0, 90, 120, self.x, self.y)

        if self.Run:
            clear_canvas()

            if self.direction == 0 or self.direction == 1:
                self.Run_y.clip_draw(self.Run_frame_y * 90, dir_to_frame(self.direction) * 120, 90, 120, self.x, self.y)
            elif self.direction == 2 or self.direction == 3:
                self.Run_x.clip_draw(self.Run_frame_x * 115, dir_to_frame(self.direction) * 120, 115, 120, self.x, self.y)

        if self.Roll:
            clear_canvas()

            if self.direction == 0 or self.direction == 1:
                self.Roll_y.clip_draw(self.Roll_frame_y * 90, dir_to_frame(self.direction) * 120, 90, 120, self.x, self.y)
            elif self.direction == 2 or self.direction == 3:
                self.Roll_x.clip_draw(self.Roll_frame_x * 100, dir_to_frame(self.direction) * 120, 100, 120, self.x, self.y)

        if self.Attack:
            clear_canvas()

            if self.direction == 0 or self.direction == 1:
                self.Attack_y.clip_draw(self.Attack_frame_y * 190, dir_to_frame(self.direction) * 265, 190, 265, self.x, self.y)
            elif self.direction == 2 or self.direction == 3:
                self.Attack_x.clip_draw(self.Attack_frame_x * 270, dir_to_frame(self.direction) * 185, 270, 185, self.x, self.y)

# 적 객체 생성


# 초기화
open_canvas(width, height)
Link = MainCharacter()


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
            elif event.key == SDLK_w or event.key == SDLK_s or event.key == SDLK_d or event.key == SDLK_a:
                run_kd(event.key)
            elif event.key == SDLK_l and not Link.Attack:
                Link.Roll = True
            elif event.key == SDLK_j and not Link.Roll:
                Link.Attack = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w or event.key == SDLK_s or event.key == SDLK_d or event.key == SDLK_a:
                run_ku(event.key)

    if dir_x == 0 and dir_y == 0:
        Link.Run = False
    else:
        Link.Run = True

        if not (Link.Roll or Link.Attack):
            if dir_y > 0 and dir_x >= 0:
                Link.direction = 0
            elif dir_y < 0 and dir_x <= 0:
                Link.direction = 1
            elif dir_x > 0 >= dir_y:
                Link.direction = 2
            elif dir_x < 0 <= dir_y:
                Link.direction = 3

    Link.draw()
    update_canvas()

    Link.update()

    delay(0.05)

close_canvas()
