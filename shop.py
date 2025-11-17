from pico2d import *
import framework
import random

#merchant frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

merchant_list = ['sprite/merchant1.png', 'sprite/merchant2.png']

class Shop:
    def __init__(self):
        self.frame = 0
        self.merchant_image = load_image(merchant_list[random.randint(0, 1)])
        self.shop_image = load_image('sprite/shop.png')
        self.shop_x, self.shop_y = 800, 440

    def draw(self):
        self.merchant_image.clip_draw(int(self.frame) * 64, 0, 64, 64, self.shop_x - 130, self.shop_y - 40, 100, 100)
        self.shop_image.clip_draw(0, 0, 166, 184, self.shop_x, self.shop_y, 166, 184)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 8

    def get_bb(self):
        return self.shop_x - 170, self.shop_y - 110, self.shop_x + 100, self.shop_y + 100

    def handle_collision(self, group, other):
        pass