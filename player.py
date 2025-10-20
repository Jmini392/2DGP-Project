from pico2d import *



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
            self.player.image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 128, 128)

class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = -1
        self.frame = 0
        self.image = load_image('idle.png')
        self.idle = Idle(self)

    def update(self):
        self.idle.do()

    def draw(self):
        self.idle.draw()