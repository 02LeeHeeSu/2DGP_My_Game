from pico2d import *

import game_framework
import game_world

import server

IsGetBow = False
IsGetShield = False
IsGetPotion = False
IsGetRobe = False
IsGetLife = [False, False, False]
selected_num = 1

PotionCoolTime = 0.0
RobeCoolTime = 0.0
Activated_Robe_Time = 0.0
is_activated_robe = False

number_of_got_life = 0


one, two, three, four = range(4)
event_name = ['one', 'two', 'three', 'four']

key_event_table = {
    (SDL_KEYDOWN, SDLK_1): one,
    (SDL_KEYDOWN, SDLK_2): two,
    (SDL_KEYDOWN, SDLK_3): three,
    (SDL_KEYDOWN, SDLK_4): four
}


def init_slot():
    global IsGetBow, IsGetShield, IsGetPotion, IsGetRobe, IsGetLife
    global selected_num
    global PotionCoolTime, RobeCoolTime, Activated_Robe_Time, is_activated_robe, number_of_got_life

    IsGetBow = False
    IsGetShield = False
    IsGetPotion = False
    IsGetRobe = False
    IsGetLife = [False, False, False]
    selected_num = 1

    PotionCoolTime = 0.0
    RobeCoolTime = 0.0
    Activated_Robe_Time = 0.0
    is_activated_robe = False

    number_of_got_life = 0



class SELECTION:
    @staticmethod
    def enter(self, event):
        global selected_num

        if event == one:
            selected_num = 1
        elif event == two:
            selected_num = 2
        elif event == three:
            selected_num = 3
        elif event == four:
            selected_num = 4

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        global PotionCoolTime, RobeCoolTime, Activated_Robe_Time, is_activated_robe
        if PotionCoolTime > 0:
            PotionCoolTime -= game_framework.frame_time
            if PotionCoolTime <= 0:
                PotionCoolTime = 0.0

        if RobeCoolTime > 0:
            RobeCoolTime -= game_framework.frame_time
            if RobeCoolTime <= 0:
                RobeCoolTime = 0.0

            Activated_Robe_Time -= game_framework.frame_time
            if Activated_Robe_Time <= 0:
                Activated_Robe_Time = 0.0

                if is_activated_robe:
                    is_activated_robe = False
                    game_world.add_collision_group(server.link, None, 'Link:Rock')
                    game_world.add_collision_group(server.link, None, 'Link:Monster')
                    game_world.add_collision_group(server.link, None, 'Link:Sphere')

    @staticmethod
    def draw(self):
        self.slot.draw(720, 50)

        if IsGetBow:
            self.Bow.draw(self.slot_x + self.slot_gap * 1, self.slot_y)
        if IsGetShield:
            self.Shield.draw(self.slot_x + self.slot_gap * 2, self.slot_y)
        if IsGetPotion:
            self.Potion.draw(self.slot_x + self.slot_gap * 3, self.slot_y)
        if IsGetRobe:
            self.Robe.draw(self.slot_x + self.slot_gap * 4, self.slot_y)
        for i in range(number_of_got_life):
            self.Life.draw(self.slot_x + self.slot_gap * (i + 5), self.slot_y)
        self.selected.draw(self.slot_x + self.slot_gap * selected_num, self.slot_y)

    
next_state = {
    SELECTION: {one: SELECTION, two: SELECTION, three: SELECTION, four: SELECTION}
}
    

class Slot:
    def __init__(self):
        global PotionCoolTime
        PotionCoolTime = 0.0

        self.queue = []
        self.cur_state = SELECTION
        self.cur_state.enter(self, None)

        self.size = 30
        self.font = load_font('Font/ENCR10B.TTF', self.size)

        self.slot_gap = 54
        self.slot_x = 557 - self.slot_gap
        self.slot_y = 65
        self.slot = load_image('Slot/slot.png')
        self.selected = load_image('Slot/selected.png')
        self.Bow = load_image('Slot/bow_slot.png')
        self.Shield = load_image('Slot/Shield_slot.png')
        self.Potion = load_image('Slot/potion_slot.png')
        self.Robe = load_image('Slot/robe_slot.png')
        self.Life = load_image('Slot/life_slot.png')

    def update(self):
        self.cur_state.do(self)

        if self.queue:
            event = self.queue.pop()
            self.cur_state.exit(self)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print(f'ERROR: State {self.cur_state.__name__}    Event {event_name[event]}')
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        if PotionCoolTime > 0:
            self.font.draw(self.slot_x + self.slot_gap * 3 - 5 * 3, 120, f'{PotionCoolTime:.0f}', (255, 255, 0))
        if RobeCoolTime > 0:
            self.font.draw(self.slot_x + self.slot_gap * 4 - 5 * 4, 120, f'{RobeCoolTime:.0f}', (255, 255, 255))
        if Activated_Robe_Time > 0:
            sx, sy = server.link.x - server.bg.window_left, server.link.y - server.bg.window_bottom
            self.font.draw(sx, sy + 60, f'{Activated_Robe_Time:.0f}', (255, 255, 255))

    def add_event(self, event):
        self.queue.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
