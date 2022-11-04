from pico2d import *


width, height = 1440, 960


# 주인공 객체 생성
# 이벤트 정의
wd, sd, dd, ad, wu, su, du, au = range(8)
key_event_table = {
    (SDL_KEYDOWN, SDLK_w): wd,
    (SDL_KEYDOWN, SDLK_s): sd,
    (SDL_KEYDOWN, SDLK_d): dd,
    (SDL_KEYDOWN, SDLK_a): ad,
    (SDL_KEYUP, SDLK_w): wu,
    (SDL_KEYUP, SDLK_s): su,
    (SDL_KEYUP, SDLK_d): du,
    (SDL_KEYUP, SDLK_a): au
}


# 클래스를 이용해서 상태를 만든다
class Stand:
    @staticmethod
    def enter(self, event):
    @staticmethod
    def exit(self):
        pass
    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        self.Stand_image.clip_draw(self.direction * 90, 0, 90, 120, self.x, self.y)
class MainCharacter:
    def __init__(self):
        self.x, self.y = width // 2, height // 2   # 위치

        self.direction = 1  # 방향

        self.Stand = load_image('Link/Stand/Stand.png')    # 서 있는 상태

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

        self.Spin = False
        self.Spin_Attack = load_image('Link/Attack/spin_attack.png')
        self.Spin_frame = 0

    def update(self):
        if self.Run and not(self.Roll or self.Attack or self.Spin):
            self.x += dir_x * 15
            self.y += dir_y * 15

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

        if self.Spin:
            self.Spin_frame = (self.Spin_frame + 1) % 13
            if self.Spin_frame == 0:
                self.Spin = False
                self.direction = 1

        if self.x < 45:
            self.x = 45
        elif self.x > width - 45:
            self.x = width - 45

        if self.y < 60:
            self.y = 60
        elif self.y > height - 60:
            self.y = height - 60

    def draw(self):
        if not (self.Run or self.Roll or self.Attack or self.Spin):
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
                self.Attack_y.clip_draw(self.Attack_frame_y * 230, dir_to_frame(self.direction) * 265, 230, 265, self.x, self.y)
            elif self.direction == 2 or self.direction == 3:
                self.Attack_x.clip_draw(self.Attack_frame_x * 240, dir_to_frame(self.direction) * 225, 240, 225, self.x, self.y)

        if self.Spin:
            clear_canvas()

            self.Spin_Attack.clip_draw(self.Spin_frame * 300, 0, 300, 255, self.x, self.y)


def handle_events():
    global selected_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.push_state(pause_state)
            elif event.key == SDLK_w or event.key == SDLK_s or event.key == SDLK_d or event.key == SDLK_a:
                run_kd(event.key)
            elif event.key == SDLK_l and not (Link.Attack or Link.Spin):
                Link.Roll = True
            elif event.key == SDLK_j and not (Link.Roll or Link.Spin):
                Link.Attack = True
            elif event.key == SDLK_k and not (Link.Roll or Link.Attack):
                Link.Spin = True
            elif event.key == SDLK_u:
                if selected_num == 1 and IsGetBow:
                    bow.Use = True
            elif event.key == SDLK_1:
                selected_num = 1
            elif event.key == SDLK_2:
                selected_num = 2
            elif event.key == SDLK_3:
                selected_num = 3
            elif event.key == SDLK_4:
                selected_num = 4
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w or event.key == SDLK_s or event.key == SDLK_d or event.key == SDLK_a:
                run_ku(event.key)
            elif event.key == SDLK_u:
                if selected_num == 1 and bow.Use:
                    bow.Use = False
