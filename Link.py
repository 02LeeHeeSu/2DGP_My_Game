from pico2d import *


width, height = 1440, 960


def dir_to_frame(direction):
    if direction < 2:
        return -direction + 1
    else:
        return -direction + 3


# 이벤트 정의
wd, sd, dd, ad, wu, su, du, au, dir_0 = range(9)
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
class STAND:
    @staticmethod
    def enter(self, event):
        self.dir_x = 0
        self.dir_y = 0
        print("stand 상태 호출")

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        self.Stand_image.clip_draw(self.direction * 90, 0, 90, 120, self.x, self.y)


class RUN:
    @staticmethod
    def enter(self, event):
        if event == wd:
            self.dir_y += 1
        elif event == sd:
            self.dir_y -= 1
        elif event == dd:
            self.dir_x += 1
        elif event == ad:
            self.dir_x -= 1
            print(f"down 호출{self.dir_x}")

        elif event == wu:
            self.dir_y -= 1
        elif event == su:
            self.dir_y += 1
        elif event == du:
            self.dir_x -= 1
        elif event == au:
            self.dir_x += 1
            print(f"up 호출{self.dir_x}")

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        # 방향 설정
        if self.dir_x == 0 and self.dir_y == 0 and self.is_none_event(self):
            self.add_event(dir_0)
        if self.dir_y > 0:
            self.direction = 0
        elif self.dir_y < 0:
            self.direction = 1
        elif self.dir_x > 0:
            self.direction = 2
        elif self.dir_x < 0:
            self.direction = 3

        # 좌표 설정
        self.x += self.dir_x * 15
        self.y += self.dir_y * 15
        self.x = clamp(45, self.x, width - 45)
        self.y = clamp(60, self.y, height - 60)

        # 프레임 변화
        self.Run_frame_x = (self.Run_frame_x + 1) % 10
        self.Run_frame_y = (self.Run_frame_y + 1) % 10

    @staticmethod
    def draw(self):
        if self.direction == 0 or self.direction == 1:
            self.Run_y_image.clip_draw(self.Run_frame_y * 90, dir_to_frame(self.direction) * 120, 90, 120, self.x, self.y)
        elif self.direction == 2 or self.direction == 3:
            self.Run_x_image.clip_draw(self.Run_frame_x * 115, dir_to_frame(self.direction) * 120, 115, 120, self.x, self.y)


next_state = {
    STAND: {wd: RUN, sd: RUN, dd: RUN, ad: RUN,
            wu: RUN, su: RUN, du: RUN, au: RUN,
            dir_0: STAND},
    RUN: {wd: RUN, sd: RUN, dd: RUN, ad: RUN,
          wu: RUN, su: RUN, du: RUN, au: RUN,
          dir_0: STAND}
}


class MainCharacter:

    def add_event(self, event):
        self.queue.insert(0, event)

    def is_none_event(self):
        if not self.queue:
            return True
        else:
            return False

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def __init__(self):
        self.queue = []
        self.cur_state = STAND
        self.cur_state.enter(self, None)

        self.x, self.y = width // 2, height // 2   # 위치

        self.direction = 1  # 방향
        self.dir_x, self.dir_y = 0, 0

        self.Stand_image = load_image('Link/Stand/Stand.png')    # 서 있는 상태

        self.Run = False
        self.Run_x_image = load_image('Link/Run/run_x.png')   # 달리기
        self.Run_y_image = load_image('Link/Run/run_y.png')
        self.Run_frame_x, self.Run_frame_y = 0, 0

        self.Roll = False
        self.Roll_x_image = load_image('Link/Roll/roll_x.png')    # 구르기
        self.Roll_y_image = load_image('Link/Roll/roll_y.png')
        self.Roll_frame_x, self.Roll_frame_y = 0, 0

        self.Attack = False
        self.Attack_x_image = load_image('Link/Attack/attack_x.png')  # 공격
        self.Attack_y_image = load_image('Link/Attack/attack_y.png')
        self.Attack_frame_x, self.Attack_frame_y = 0, 0

        self.Spin = False
        self.Spin_Attack_image = load_image('Link/Attack/spin_attack.png')
        self.Spin_frame = 0

    def update(self):
        self.cur_state.do(self)

        if self.queue:
            event = self.queue.pop()
            self.cur_state.exit(self)
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)
        # if self.Run and not(self.Roll or self.Attack or self.Spin):
        #     self.x += self.dir_x * 15
        #     self.y += self.dir_y * 15
        #
        #     self.Run_frame_x = (self.Run_frame_x + 1) % 10
        #     self.Run_frame_y = (self.Run_frame_y + 1) % 10

        # if self.Roll:
        #     if self.direction == 0 or self.direction == 1:
        #         if self.direction == 0:
        #             self.y += 20
        #         else:
        #             self.y -= 20
        #
        #         self.Roll_frame_y = (self.Roll_frame_y + 1) % 9
        #         if self.Roll_frame_y == 0:
        #             self.Roll = False
        #     elif self.direction == 2 or self.direction == 3:
        #         if self.direction == 2:
        #             self.x += 18
        #         else:
        #             self.x -= 18
        #
        #         self.Roll_frame_x = (self.Roll_frame_x + 1) % 10
        #         if self.Roll_frame_x == 0:
        #             self.Roll = False
        #
        # if self.Attack:
        #     if self.direction == 0 or self.direction == 1:
        #         self.Attack_frame_y = (self.Attack_frame_y + 1) % 7
        #         if self.Attack_frame_y == 0:
        #             self.Attack = False
        #     elif self.direction == 2 or self.direction == 3:
        #         self.Attack_frame_x = (self.Attack_frame_x + 1) % 7
        #         if self.Attack_frame_x == 0:
        #             self.Attack = False
        #
        # if self.Spin:
        #     self.Spin_frame = (self.Spin_frame + 1) % 13
        #     if self.Spin_frame == 0:
        #         self.Spin = False
        #         self.direction = 1

        # if self.x < 45:
        #     self.x = 45
        # elif self.x > width - 45:
        #     self.x = width - 45
        #
        # if self.y < 60:
        #     self.y = 60
        # elif self.y > height - 60:
        #     self.y = height - 60

    def draw(self):
        self.cur_state.draw(self)
        # if not (self.Run or self.Roll or self.Attack or self.Spin):
        #     self.Stand.clip_draw(self.direction * 90, 0, 90, 120, self.x, self.y)

        # if self.Run:
        #     clear_canvas()
        #
        #     if self.direction == 0 or self.direction == 1:
        #         self.Run_y.clip_draw(self.Run_frame_y * 90, dir_to_frame(self.direction) * 120, 90, 120, self.x, self.y)
        #     elif self.direction == 2 or self.direction == 3:
        #         self.Run_x.clip_draw(self.Run_frame_x * 115, dir_to_frame(self.direction) * 120, 115, 120, self.x, self.y)

        # if self.Roll:
        #     clear_canvas()
        #
        #     if self.direction == 0 or self.direction == 1:
        #         self.Roll_y_image.clip_draw(self.Roll_frame_y * 90, dir_to_frame(self.direction) * 120, 90, 120, self.x, self.y)
        #     elif self.direction == 2 or self.direction == 3:
        #         self.Roll_x_image.clip_draw(self.Roll_frame_x * 100, dir_to_frame(self.direction) * 120, 100, 120, self.x, self.y)
        #
        # if self.Attack:
        #     clear_canvas()
        #
        #     if self.direction == 0 or self.direction == 1:
        #         self.Attack_y.clip_draw(self.Attack_frame_y * 230, dir_to_frame(self.direction) * 265, 230, 265, self.x, self.y)
        #     elif self.direction == 2 or self.direction == 3:
        #         self.Attack_x_image.clip_draw(self.Attack_frame_x * 240, dir_to_frame(self.direction) * 225, 240, 225, self.x, self.y)
        #
        # if self.Spin:
        #     clear_canvas()
        #
        #     self.Spin_Attack.clip_draw(self.Spin_frame * 300, 0, 300, 255, self.x, self.y)
