from pico2d import *
import framework

#merchant frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Merchant:
    image = None
    def __init__(self):
        self.x, self.y = 500, 300
        self.frame = 0
        if Merchant.image is None:
            Merchant.image = load_image('sprite/merchant2.png')

    def draw(self):
        self.image.clip_draw(int(self.frame) * 64, 0, 64, 64, self.x, self.y, 100, 100)

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 8