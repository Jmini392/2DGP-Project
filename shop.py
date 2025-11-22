from pico2d import *
import framework
import random

#merchant frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

merchant_list = ['sprite/merchant1.png', 'sprite/merchant2.png']
merchant_index = 0

class Shop:
    def __init__(self):
        self.frame = 0
        self.merchant_index = random.randint(0, 1)
        global merchant_index
        merchant_index = self.merchant_index
        self.merchant_image = load_image(merchant_list[self.merchant_index])
        self.shop_image = load_image('sprite/shop.png')
        self.shop_x, self.shop_y = 1000, 340

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

class Stand:
    def __init__(self):
        self.merchant_img = load_image(f'sprite/merchant{merchant_index + 1}.png')
        self.image = load_image('sprite/stand.png')
        self.frame = 0

    def draw(self):
        self.merchant_img.clip_draw(int(self.frame) * 64, 0, 64, 64, 990, 400, 600, 600)
        self.image.clip_draw(0, 0, 166, 184, 720, 350, 1494, 1656)

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 8
