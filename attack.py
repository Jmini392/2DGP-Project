from pico2d import *

class Attack:
    def __init__(self, player, damage = 10):
        self.player = player
        self.face_dir = player.face_dir
        self.x, self.y = player.x, player.y + 25
        self.p_cnt = player.ATTACK.punch
        self.k_cnt = player.ATTACK.kick
        self.kick = player.kick
        if self.kick:
            self.damage = damage + 10 * (self.k_cnt + 1)
        else:
            self.damage = damage + 5 ** (self.p_cnt + 1)

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x, self.y = self.player.x, self.player.y + 25

    def get_bb(self):
        if self.kick:
            if self.face_dir == 1:
                return self.x + 30, self.y - 90, self.x + 100, self.y
            else:
                return self.x - 100, self.y - 90, self.x - 30, self.y
        else:
            if self.face_dir == 1:
                return self.x + 30, self.y - 30, self.x + 80, self.y + 10
            else:
                return self.x - 80, self.y - 30, self.x - 30, self.y + 10

    def handle_collision(self, group, other):
        pass