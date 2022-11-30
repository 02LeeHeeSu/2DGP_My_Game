from pico2d import *
import game_framework
import game_world

from define_dir import defined_direction
from define_PPM import Pixel_Per_Sec_link
from depth import level

import heart
from sword import Sword
from arrow import Arrow
import slot
from heart import cur_hp, max_hp

from canvas_size import width, height

# 방향
direction = defined_direction['down']

PPS_Roll = 1.5 * Pixel_Per_Sec_link
PPS_Arrow = 4.0 * Pixel_Per_Sec_link

# 달리기 속도
Time_Per_Run = 0.5
Run_Per_Time = 1.0 / Time_Per_Run
FPRun = 10

# 구르기 속도
Time_Per_Roll = 0.5
Roll_Per_Time = 1 / Time_Per_Roll
FPRoll = 9

# 공격 속도
Time_Per_Attack = 0.3
Attack_Per_Time = 1 / Time_Per_Attack
FPAttack = 7

# 회전공격 속도
Time_Per_Spin = 0.6
Spin_Per_Time = 1 / Time_Per_Spin
FPSpin = 13


# 활 사용 속도
Time_Per_Bow = 1.0
Bow_Per_Time = 1.0 / Time_Per_Bow
FPBow = 10


# 방패 사용 속도
Time_Per_Shield = 0.2
Shield_Per_Time = 1.0 / Time_Per_Shield
FPShield = 5


# 사망 액션 속도
Time_Per_Die = 0.5
Die_Per_Time = 1.0 / Time_Per_Die
FPDie = 5


def dir_to_frame(d):
    if d < 2:
        return -d + 1
    else:
        return -d + 3


# 이벤트 정의
wd, sd, dd, ad, wu, su, du, au, jd, kd, ld, ud, uu, dir_0 = range(14)
event_name = ['wd', 'sd', 'dd', 'ad',
              'wu', 'su', 'du', 'au',
              'jd', 'kd', 'ld',
              'ud', 'uu',
              'dir_0']

key_event_table = {
    (SDL_KEYDOWN, SDLK_w): wd,
    (SDL_KEYDOWN, SDLK_s): sd,
    (SDL_KEYDOWN, SDLK_d): dd,
    (SDL_KEYDOWN, SDLK_a): ad,
    (SDL_KEYUP, SDLK_w): wu,
    (SDL_KEYUP, SDLK_s): su,
    (SDL_KEYUP, SDLK_d): du,
    (SDL_KEYUP, SDLK_a): au,
    (SDL_KEYDOWN, SDLK_j): jd,
    (SDL_KEYDOWN, SDLK_k): kd,
    (SDL_KEYDOWN, SDLK_l): ld,
    (SDL_KEYDOWN, SDLK_u): ud,
    (SDL_KEYUP, SDLK_u): uu
}


# 클래스를 이용해서 상태를 만든다
class STAND:
    @staticmethod
    def enter(self, event):
        self.dir_x = 0
        self.dir_y = 0

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        pass

    @staticmethod
    def draw(self):
        self.Stand_image.clip_draw(direction * 90, 0, 90, 120, self.x, self.y)


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

        elif event == wu or event == su:
            self.dir_y = 0
        elif event == du or event == au:
            self.dir_x = 0

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        global direction

        # 방향 설정
        if self.dir_x == 0 and self.dir_y == 0 and self.is_none_event():
            self.convert_to_stand()
        if self.dir_y > 0:
            direction = defined_direction['up']
        elif self.dir_y < 0:
            direction = defined_direction['down']
        elif self.dir_x > 0:
            direction = defined_direction['right']
        elif self.dir_x < 0:
            direction = defined_direction['left']

        # 좌표 설정
        self.x += self.dir_x * Pixel_Per_Sec_link * game_framework.frame_time
        self.y += self.dir_y * Pixel_Per_Sec_link * game_framework.frame_time
        self.x = clamp(45, self.x, width - 45)
        self.y = clamp(60, self.y, height - 60)

        # 프레임 변화
        self.Run_frame_x = (self.Run_frame_x + FPRun * Run_Per_Time * game_framework.frame_time) % FPRun
        self.Run_frame_y = (self.Run_frame_y + FPRun * Run_Per_Time * game_framework.frame_time) % FPRun

    @staticmethod
    def draw(self):
        global direction

        if direction == defined_direction['up'] or direction == defined_direction['down']:
            self.Run_y_image.clip_draw(int(self.Run_frame_y) * 90, dir_to_frame(direction) * 120, 90, 120, self.x, self.y)
        elif direction == defined_direction['right'] or direction == defined_direction['left']:
            self.Run_x_image.clip_draw(int(self.Run_frame_x) * 115, dir_to_frame(direction) * 120, 115, 120, self.x, self.y)


class ACTION:
    sword_obj = None

    @staticmethod
    def enter(self, event):
        if self.is_none_action():
            if event == jd:
                self.Attack = True
            elif event == kd:
                self.Spin = True
            elif event == ld:
                self.Roll = True

    @staticmethod
    def exit(self, event):
        pass

    @staticmethod
    def do(self):
        global direction

        if self.Attack or self.Spin:
            if ACTION.sword_obj is None:
                ACTION.sword_obj = Sword(direction)
                game_world.add_object(ACTION.sword_obj, 1)
                game_world.add_collision_group(ACTION.sword_obj, None, 'Sword:ChuChu')
                game_world.add_collision_group(ACTION.sword_obj, None, 'Sword:Octorok')

        if self.Attack:
            if direction == defined_direction['up'] or direction == defined_direction['down']:
                if self.Attack_frame_y >= FPAttack - 1:
                    for obj in game_world.world[level['Sword']]:
                        if obj == ACTION.sword_obj:
                            game_world.remove_object(ACTION.sword_obj, level['Sword'])
                    ACTION.sword_obj = None
                    self.Attack = False
                    self.Attack_frame_y = 0
                    self.convert_to_stand()

                self.Attack_frame_y = (self.Attack_frame_y + FPAttack * Attack_Per_Time * game_framework.frame_time) % FPAttack

            elif direction == defined_direction['right'] or direction == defined_direction['left']:
                if self.Attack_frame_x >= FPAttack - 1:
                    for obj in game_world.world[level['Sword']]:
                        if obj == ACTION.sword_obj:
                            game_world.remove_object(ACTION.sword_obj, level['Sword'])
                    ACTION.sword_obj = None
                    self.Attack = False
                    self.Attack_frame_x = 0
                    self.convert_to_stand()

                self.Attack_frame_x = (self.Attack_frame_x + FPAttack * Attack_Per_Time * game_framework.frame_time) % FPAttack

        if self.Spin:
            if self.Spin_frame >= FPSpin - 1:
                for obj in game_world.world[level['Sword']]:
                    if obj == ACTION.sword_obj:
                        game_world.remove_object(ACTION.sword_obj, level['Sword'])
                ACTION.sword_obj = None
                self.Spin = False
                self.Spin_frame = 0
                direction = 1
                self.convert_to_stand()

            self.Spin_frame = (self.Spin_frame + FPSpin * Spin_Per_Time * game_framework.frame_time) % FPSpin

        if self.Roll:
            if direction == defined_direction['up'] or direction == defined_direction['down']:
                if direction == defined_direction['up']:
                    self.y += PPS_Roll * game_framework.frame_time
                else:
                    self.y -= PPS_Roll * game_framework.frame_time

                if self.Roll_frame_y > FPRoll - 1:
                    self.Roll = False
                    self.Roll_frame_y = 0
                    self.convert_to_stand()

                self.Roll_frame_y = (self.Roll_frame_y + FPRoll * Roll_Per_Time * game_framework.frame_time) % FPRoll

            elif direction == defined_direction['right'] or direction == defined_direction['left']:
                if direction == defined_direction['right']:
                    self.x += PPS_Roll * game_framework.frame_time
                else:
                    self.x -= PPS_Roll * game_framework.frame_time

                if self.Roll_frame_x > FPRoll - 1:
                    self.Roll = False
                    self.Roll_frame_x = 0
                    self.convert_to_stand()

                self.Roll_frame_x = (self.Roll_frame_x + FPRoll * Roll_Per_Time * game_framework.frame_time) % FPRoll

            self.x = clamp(45, self.x, width - 45)
            self.y = clamp(60, self.y, height - 60)

    @staticmethod
    def draw(self):
        if self.Attack:
            if direction == defined_direction['up'] or direction == defined_direction['down']:
                self.Attack_y_image.clip_draw(int(self.Attack_frame_y) * 230, dir_to_frame(direction) * 265, 230, 265, self.x, self.y)
            elif direction == defined_direction['right'] or direction == defined_direction['left']:
                self.Attack_x_image.clip_draw(int(self.Attack_frame_x) * 240, dir_to_frame(direction) * 225, 240, 225, self.x, self.y)

        if self.Spin:
            self.Spin_Attack_image.clip_draw(int(self.Spin_frame) * 300, 0, 300, 255, self.x, self.y - 25)

        if self.Roll:
            if direction == defined_direction['up'] or direction == defined_direction['down']:
                self.Roll_y_image.clip_draw(int(self.Roll_frame_y) * 90, dir_to_frame(direction) * 120, 90, 120, self.x, self.y)
            elif direction == defined_direction['right'] or direction == defined_direction['left']:
                self.Roll_x_image.clip_draw(int(self.Roll_frame_x) * 100, dir_to_frame(direction) * 120, 100, 120, self.x, self.y)


class ITEM:
    enter_time = None
    exit_time = None

    @staticmethod
    def enter(self, event):
        ITEM.enter_time = get_time()

        self.Bow_frame_x = 0
        self.Bow_frame_y = 0

        self.Shield_frame_x = 0
        self.Shield_frame_y = 0

    @staticmethod
    def exit(self, event):
        if event == uu:
            ITEM.exit_time = get_time()
            overtime = ITEM.exit_time - ITEM.enter_time

            if slot.selected_num == 1 and slot.IsGetBow:
                self.Bow_frame_x = 0
                self.Bow_frame_y = 0

                arrow_obj = Arrow(self.x, self.y, PPS_Arrow, direction, overtime)
                game_world.add_object(arrow_obj, 1)

                game_world.add_collision_group(arrow_obj, None, 'Arrow:ChuChu')
                game_world.add_collision_group(arrow_obj, None, 'Arrow:Octorok')

    @staticmethod
    def do(self):
        # 활
        if slot.selected_num == 1 and slot.IsGetBow:
            if direction == defined_direction['up'] or direction == defined_direction['down']:
                if self.Bow_frame_y >= FPBow - 1:
                    self.Bow_frame_y = 9

                self.Bow_frame_y = (self.Bow_frame_y + FPBow * Bow_Per_Time * game_framework.frame_time) % FPBow

            elif direction == defined_direction['right'] or direction == defined_direction['left']:
                if self.Bow_frame_x >= FPBow - 1:
                    self.Bow_frame_x = 9

                self.Bow_frame_x = (self.Bow_frame_x + FPBow * Bow_Per_Time * game_framework.frame_time) % FPBow

        # 방패
        if slot.selected_num == 2 and slot.IsGetShield:
            if direction == defined_direction['up'] or direction == defined_direction['down']:
                if self.Shield_frame_y >= FPShield - 1:
                    self.Shield_frame_y = 4

                self.Shield_frame_y = (self.Shield_frame_y + FPShield * Shield_Per_Time * game_framework.frame_time) % FPShield

            elif direction == defined_direction['right'] or direction == defined_direction['left']:
                if self.Shield_frame_x >= FPShield - 1:
                    self.Shield_frame_x = 4

                self.Shield_frame_x = (self.Shield_frame_x + FPShield * Shield_Per_Time * game_framework.frame_time) % FPShield

        if slot.selected_num == 3 and slot.IsGetPotion:
            if slot.PotionCoolTime == 0.0:
                slot.PotionCoolTime = 5.0
                self.current += self.maximum // 4
                self.current = clamp(0, self.current, self.maximum)
                heart.cur_hp = self.current
                heart.max_hp = self.maximum
            self.convert_to_stand()

    @staticmethod
    def draw(self):
        # 활
        if slot.selected_num == 1 and slot.IsGetBow:
            if direction == defined_direction['up'] or direction == defined_direction['down']:
                self.Bow_y_image.clip_draw(int(self.Bow_frame_y) * 140, dir_to_frame(direction) * 130, 140, 130, self.x, self.y)

            elif direction == defined_direction['right']:
                self.Bow_x_image.clip_composite_draw(int(self.Bow_frame_x) * 140, 0, 140, 130,
                                                     0, '', self.x, self.y, 140, 130)

            elif direction == defined_direction['left']:
                self.Bow_x_image.clip_composite_draw(int(self.Bow_frame_x) * 140, 0, 140, 130,
                                                     0, 'h', self.x, self.y, 140, 130)

        elif not slot.IsGetBow:
            self.Stand_image.clip_draw(direction * 90, 0, 90, 120, self.x, self.y)

        # 방패
        if slot.selected_num == 2 and slot.IsGetShield:
            if direction == defined_direction['up'] or direction == defined_direction['down']:
                self.Shield_y_image.clip_draw(int(self.Shield_frame_y) * 90, dir_to_frame(direction) * 125, 90, 125, self.x, self.y)

            elif direction == defined_direction['right']:
                self.Shield_x_image.clip_composite_draw(int(self.Shield_frame_x) * 115, 0, 115, 110, 0, 'h', self.x, self.y, 115, 110)

            elif direction == defined_direction['left']:
                self.Shield_x_image.clip_composite_draw(int(self.Shield_frame_x) * 115, 0, 115, 110, 0, '', self.x, self.y, 115, 110)

        elif not slot.IsGetShield:
            self.Stand_image.clip_draw(direction * 90, 0, 90, 120, self.x, self.y)

        if slot.selected_num == 3 and slot.IsGetPotion:
            self.Stand_image.clip_draw(direction * 90, 0, 90, 120, self.x, self.y)


next_state = {
    STAND: {wd: RUN, sd: RUN, dd: RUN, ad: RUN,
            wu: STAND, su: STAND, du: STAND, au: STAND,
            dir_0: STAND,
            jd: ACTION, kd: ACTION, ld: ACTION,
            ud: ITEM, uu: STAND},
    RUN: {wd: RUN, sd: RUN, dd: RUN, ad: RUN,
          wu: RUN, su: RUN, du: RUN, au: RUN,
          dir_0: STAND,
          jd: ACTION, kd: ACTION, ld: ACTION,
          ud: ITEM, uu: RUN},
    ACTION: {wd: ACTION, sd: ACTION, dd: ACTION, ad: ACTION,
             wu: ACTION, su: ACTION, du: ACTION, au: ACTION,
             dir_0: STAND,
             jd: ACTION, kd: ACTION, ld: ACTION,
             ud: ACTION, uu: ACTION},

    ITEM: {wd: RUN, sd: RUN, dd: RUN, ad: RUN,
           wu: STAND, su: STAND, du: STAND, au: STAND,
           dir_0: STAND,
           jd: ACTION, kd: ACTION, ld: ACTION,
           ud: ITEM, uu: STAND}
}


class MainCharacter:

    def add_event(self, event):
        self.queue.insert(0, event)

    def convert_to_stand(self):
        self.add_event(dir_0)

    def is_none_event(self):
        if not self.queue:
            return True
        else:
            return False

    def is_none_action(self):
        if not (self.Attack or self. Spin or self.Roll):
            return True
        else:
            return False

    def get_bb(self):
        return self.x - 45, self.y - 60, self.x + 45, self.y + 60

    def handle_collision(self, other, group):
        if group == 'Link:ChuChu':
            self.current -= 1
            self.current = clamp(0, self.current, self.maximum)
            heart.cur_hp = self.current

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def __init__(self):
        self.queue = []
        self.cur_state = STAND
        self.cur_state.enter(self, None)

        self.maximum = heart.max_hp
        self.current = heart.cur_hp
        self.current = clamp(0, self.current, self.maximum)

        self.x, self.y = width // 2, height // 2   # 위치

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

        self.Bow_x_image = load_image('Link/Item/bow_x.png')
        self.Bow_y_image = load_image('Link/Item/bow_y.png')
        self.Bow_frame_x, self.Bow_frame_y = 0, 0

        self.Shield_x_image = load_image('Link/Item/shield_x.png')
        self.Shield_y_image = load_image('Link/Item/shield_y.png')
        self.Shield_frame_x, self.Shield_frame_y = 0, 0

        self.Die = load_image('Link/Die/die.png')
        self.Die_frame = 0

    def update(self):
        self.cur_state.do(self)

        if self.queue:
            event = self.queue.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())
