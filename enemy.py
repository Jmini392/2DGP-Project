from pico2d import *
import framework
import game_world
import item

gorgon_image = ['sprite/Gorgon_idle.png']

#enemy frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Enemy:
    def __init__(self, x = 400, y = 300, name = 'Gorgon', health = 100, attack_power = 10):
        self.x, self.y = x, y
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.frame = 0
        if name == 'Gorgon':
            self.image = load_image(gorgon_image[0])

    def draw(self):
        self.image.clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 100, self.x + 50, self.y + 30

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 4

    def handle_collision(self, group, other):
        if group == 'player:enemy':
            game_world.remove_object(self)
            # 아이템 드랍
            dropped_item = item.Item(self.x + 10, self.y - 20, 0)
            game_world.add_object(dropped_item, 1)
            game_world.add_collision_pair('player:item', None, dropped_item)