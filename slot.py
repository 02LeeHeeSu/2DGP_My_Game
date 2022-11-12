from pico2d import *

IsGetBow = True
IsGetShield = True
IsGetPotion = True
selected_num = 1


one, two, three, four = range(4)
key_event_table = {
    (SDL_KEYDOWN, SDLK_1): one,
    (SDL_KEYDOWN, SDLK_2): two,
    (SDL_KEYDOWN, SDLK_3): three,
    (SDL_KEYDOWN, SDLK_4): four
}


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
        pass

    @staticmethod
    def draw(self):
        self.slot.draw(720, 50)

        if IsGetBow:
            self.Bow.draw(self.slot_x + self.slot_gap * 1, self.slot_y)
        if IsGetShield:
            self.Shield.draw(self.slot_x + self.slot_gap * 2, self.slot_y)
        if IsGetPotion:
            self.Potion.draw(self.slot_x + self.slot_gap * 3, self.slot_y)

        self.selected.draw(self.slot_x + self.slot_gap * selected_num, self.slot_y)
    
    
next_state = {
    SELECTION: {one: SELECTION, two: SELECTION, three: SELECTION, four: SELECTION}
}
    

class Slot:
    def add_event(self, event):
        self.queue.insert(0, event)
    
    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
            
    def __init__(self):
        self.queue = []
        self.cur_state = SELECTION
        self.cur_state.enter(self, None)

        self.slot_gap = 54
        self.slot_x = 557 - self.slot_gap
        self.slot_y = 65
        self.slot = load_image('Slot/slot.png')
        self.selected = load_image('Slot/selected.png')
        self.Bow = load_image('Slot/bow_slot.png')
        self.Shield = load_image('Slot/Shield_slot.png')
        self.Potion = load_image('Slot/potion_slot.png')

    def update(self):
        self.cur_state.do(self)

        if self.queue:
            event = self.queue.pop()
            self.cur_state.exit(self)
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
