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
        self.merchant_x, self.merchant_y = 500, 300
        self.shop_x, self.shop_y = 630, 340

    def draw(self):
        self.merchant_image.clip_draw(int(self.frame) * 64, 0, 64, 64, self.merchant_x, self.merchant_y, 100, 100)
        self.shop_image.clip_draw(0, 0, 166, 184, self.shop_x, self.shop_y, 166, 184)

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 8