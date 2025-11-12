from pico2d import *

class Shop:
    def __init__(self):
        self.image = load_image('sprite/shop.png')
        self.x, self.y = 630, 340

    def draw(self):
        self.image.clip_draw(0, 0, 166, 184, self.x, self.y, 166, 184)

    def update(self):
        pass