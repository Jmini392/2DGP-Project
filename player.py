from pico2d import *

class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('idle.png')

    def update(self):
        self.frame = (self.frame + 1) % 6

    def draw(self):
        self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)