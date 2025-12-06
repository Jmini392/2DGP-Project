from pico2d import *

import game_world
import share

class Attack:
    def __init__(self):
        self.face_dir = share.player.face_dir
        self.x, self.y = share.player.x, share.player.y + 25
        self.p_cnt = share.player.ATTACK.punch_cnt
        self.k_cnt = share.player.ATTACK.kick_cnt
        self.kick = share.player.ATTACK.kick
        if share.player.is_strong_boosted():
            damage = 30
        else:
            damage = 10
        if self.kick:
            self.damage = damage * (self.k_cnt + 1) * 2
        else:
            self.damage = damage * (self.p_cnt + 1)
        self.audio = load_wav('sound/hit.wav')
        self.audio.set_volume(100)
        self.play = False

    def draw(self):
        pass

    def update(self):
        self.x, self.y = share.player.x, share.player.y + 25

    def get_bb(self):
        if self.kick:
            if self.face_dir == 1:
                return self.x + 30, self.y - 90, self.x + 60, self.y
            else:
                return self.x - 60, self.y - 90, self.x - 30, self.y
        else:
            if self.face_dir == 1:
                return self.x + 30, self.y - 30, self.x + 80, self.y + 10
            else:
                return self.x - 80, self.y - 30, self.x - 30, self.y + 10

    def handle_collision(self, group, other):
        if group == 'attack:enemy':
            if self.play is False:
                self.audio.play()
                self.play = True