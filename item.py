from pico2d import *
import random

import game_world
import game_framework

import server

import stage_info

from depth import level


Bow, Shield, Potion, Robe, Life = range(1, 5 + 1)

Item_Queue = [Bow, Shield, Potion, Robe, Life, Life, Life]


def get_item():
    if Item_Queue:
        item = random.choice(Item_Queue)
        Item_Queue.remove(item)

        return item


class Item:
    image = None

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        return sx - 20, sy - 20, sx + 20, sy + 20

    def handle_collision(self, other, group):
        if group == 'Link:Item':
            game_world.remove_object(self, level['Objects'])

    def __init__(self):
        if Item.image is None:
            Item.image = load_image('Dropped_Item/dropped_item.png')
        self.x, self.y = 912, 224 * 6 / 2
        self.item = get_item()

    def draw(self):
        draw_rectangle(*self.get_bb())

        sx, sy = self.x - server.bg.window_left, self.y - server.bg.window_bottom

        Item.image.draw(sx, sy, 40, 40)

    def update(self):
        pass
