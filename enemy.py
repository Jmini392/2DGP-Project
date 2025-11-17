from pico2d import *
import framework
import game_world
import item
import random

gorgon1_image = ['sprite/Gorgon_idle1.png', 'sprite/Gorgon_attack1.png', 'sprite/Gorgon_die1.png']
gorgon2_image = ['sprite/Gorgon_idle2.png', 'sprite/Gorgon_attack2.png', 'sprite/Gorgon_die2.png']
gorgon3_image = ['sprite/Gorgon_idle3.png', 'sprite/Gorgon_attack3.png', 'sprite/Gorgon_die3.png']
gorgon = [gorgon1_image, gorgon2_image, gorgon3_image]

#enemy frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Gorgon:
    def __init__(self, x = 400, y = 300, type = 0):
        self.x, self.y = x, y
        self.health = 100 * (type + 1)
        self.attack_power = 10 * (type + 1)
        self.type = type
        self.attack = False
        self.die = False
        self.frame = 0
        self.font = load_font('ENCR10B.TTF', 16)
        self.idle_image = load_image(gorgon[self.type][0])
        self.attack_image = load_image(gorgon[self.type][1])
        self.die_image = load_image(gorgon[self.type][2])

    def draw(self):
        if self.attack:
            self.attack_image.clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        elif self.die:
            self.die_image.clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        else:
            self.idle_image.clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - 30, self.y + 50, f'HP: {self.health}', (255, 0, 0))

    def get_bb(self):
        return self.x - 30, self.y - 70, self.x + 40, self.y + 30

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 7

    def handle_collision(self, group, other):
        if group == 'attack:enemy':
            # 적 체력 감소
            self.health -= other.damage
            if self.health <= 0:
                self.die = True
                game_world.remove_object(self)
                # 아이템 드랍
                if (random.random() < 0.5):  # 50% 확률로 아이템 드랍
                    dropped_item = item.Item(self.x + 10, self.y - 20, random.randint(0, 2))
                    game_world.add_object(dropped_item, 1)
                    game_world.add_collision_pair('player:item', None, dropped_item)