from pico2d import *
from canvas_size import height


max_hp = 12
cur_hp = 3
cur_hp = clamp(0, cur_hp, max_hp)


def cal_integer(x):
    if int(x) % 4 == 0:
        return int(x // 4)
    else:
        return int(x) + 1


class Heart:

    def handle_event(self, event):
        pass

    def __init__(self):
        self.HeartImage = load_image('Heart/heart.png')
        self.MaximumHeartNumber = cal_integer(max_hp)   # 전체 하트 개수
        self.FullHeartNumber = cur_hp // 4  # 완전히 채워져 있는 하트 개수
        self.BrokeHeart = cur_hp % 4    # 부서진 하트의 손상 정도

    def update(self):
        self.MaximumHeartNumber = cal_integer(max_hp)
        self.FullHeartNumber = cur_hp // 4
        self.BrokeHeart = cur_hp % 4

    def draw(self):
        for i in range(0, self.FullHeartNumber):
            self.HeartImage.clip_draw(45 * 4, 0, 45, 40, 45 + 50 * i, height - 40)

        for i in range(self.FullHeartNumber + 1, self.MaximumHeartNumber):
            self.HeartImage.clip_draw(45 * 0, 0, 45, 40, 45 + 50 * i, height - 40)

        if self.MaximumHeartNumber > self.FullHeartNumber:
            self.HeartImage.clip_draw(45 * self.BrokeHeart, 0, 45, 40, 45 + 50 * self.FullHeartNumber, height - 40)
