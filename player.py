from pico2d import *
from sdl2 import *

class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8
        self.player.x += self.player.face_dir * 5
        if self.player.x < 64:
            self.player.x = 64
        elif self.player.x > 800 - 64:
            self.player.x = 800 - 64

    def draw(self):
        if self.player.face_dir == 1:
            self.player.walk_image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y)
        else:
            self.player.walk_image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 128, 128)

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 6

    def draw(self):
        if self.player.face_dir == 1:
            self.player.idel_image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y)
        else:
            self.player.idle_image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 128, 128)

class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.frame = 0
        self.idle_image = load_image('idle.png')
        self.walk_image = load_image('Walk.png')
        self.idle = Idle(self)
        self.walk = Walk(self)

    def update(self):
        # self.idle.do()
        self.walk.do()

    def draw(self):
        # self.idle.draw()
        self.walk.draw()
