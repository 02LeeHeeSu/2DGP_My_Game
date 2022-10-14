from pico2d import *

import game_framework
import title_state

width, height = 1440, 960
dir_x, dir_y = 0, 0

slot_gap = 54
slot_x = 557 - slot_gap
slot_y = 65


def set_direction():
    if dir_x == 0 and dir_y == 0:
        Link.Run = False
    else:
        Link.Run = True

        if not (Link.Roll or Link.Attack or Link.Spin):
            if dir_y > 0:
                Link.direction = 0
            elif dir_y < 0:
                Link.direction = 1
            elif dir_x > 0:
                Link.direction = 2
            elif dir_x < 0:
                Link.direction = 3


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


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_w or event.key == SDLK_s or event.key == SDLK_d or event.key == SDLK_a:
                run_kd(event.key)
            elif event.key == SDLK_l and not (Link.Attack or Link.Spin):
                Link.Roll = True
            elif event.key == SDLK_j and not (Link.Roll or Link.Spin):
                Link.Attack = True
            elif event.key == SDLK_k and not (Link.Roll or Link.Attack):
                Link.Spin = True
            elif event.key == SDLK_1:
                slot.number = 1
            elif event.key == SDLK_2:
                slot.number = 2
            elif event.key == SDLK_3:
                slot.number = 3
            elif event.key == SDLK_4:
                slot.number = 4
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_w or event.key == SDLK_s or event.key == SDLK_d or event.key == SDLK_a:
                run_ku(event.key)


# 주인공 객체 생성
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
                self.Attack_y.clip_draw(self.Attack_frame_y * 190, dir_to_frame(self.direction) * 265, 190, 265, self.x, self.y)
            elif self.direction == 2 or self.direction == 3:
                self.Attack_x.clip_draw(self.Attack_frame_x * 270, dir_to_frame(self.direction) * 225, 270, 225, self.x, self.y)

        if self.Spin:
            clear_canvas()

            self.Spin_Attack.clip_draw(self.Spin_frame * 300, 0, 300, 255, self.x, self.y)


# Item 그리고 Item slot
class Item:
    def __init__(self):
        self.slot = load_image('Item/slot.png')
        self.selected = load_image('Item/selected.png')
        self.number = 1
        self.Arrow = load_image('Item/arrow_slot.png')
        self.IsGetArrow = True
        self.Shield = load_image('Item/Shield_slot.png')
        self.IsGetShield = True
        self.Potion = load_image('Item/potion_slot.png')
        self.IsGetPotion = True

    def draw(self):
        self.slot.draw(720, 50)

        if self.IsGetArrow:
            self.Arrow.draw(slot_x + slot_gap * 1, slot_y)
        if self.IsGetShield:
            self.Shield.draw(slot_x + slot_gap * 2, slot_y)
        if self.IsGetPotion:
            self.Potion.draw(slot_x + slot_gap * 3, slot_y)

        self.selected.draw(slot_x + slot_gap * self.number, slot_y)


# 게임 초기화: 객체 생성
Link = None
slot = None


def enter():
    global Link, slot
    Link = MainCharacter()
    slot = Item()


def update():
    set_direction()
    Link.update()
    delay(0.04)


def draw():
    clear_canvas()
    Link.draw()
    slot.draw()
    update_canvas()


def end():
    global Link, slot
    del Link
    del slot


def test_self():
    import sys
    open_canvas(width, height)
    game_framework.run(sys.modules['__main__'])
    close_canvas()


if __name__ == '__main__':
    test_self()
