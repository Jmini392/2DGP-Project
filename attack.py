from pico2d import *
#zimport game_world
#import player

class Attack:
    def __init__(self, player):
        self.face_dir = player.face_dir
        self.x, self.y = player.x, player.y + 25
        self.special_attack = player.special_attack
        self.damage = 40 if self.special_attack else 10

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        if self.face_dir == 1:
            if self.special_attack:
                return self.x + 30, self.y - 60, self.x + 90, self.y
            else:
                return self.x + 30, self.y - 10, self.x + 60, self.y + 10
        else:
            if self.special_attack:
                return self.x - 30, self.y - 60, self.x - 90, self.y
            else:
                return self.x - 30, self.y - 10, self.x - 60, self.y + 10

    def handle_collision(self, group, other):
        pass