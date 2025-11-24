from pico2d import *
import framework
import game_world
import item
import random
import share
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

animation_names = ['walk', 'idle', 'attack', 'die']

#enemy speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#enemy frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Gorgon:
    image = None
    def load_images(self):
        if Gorgon.image == None:
            Gorgon.image = {}
            for i in range(3):
                Gorgon.image[i] = {}
                for name in animation_names:
                    Gorgon.image[i][name] = load_image("sprite/Gorgon_" + name + str(i + 1) + ".png")

    def __init__(self, x = 400, y = 300, type = 0):
        self.x, self.y = x, y
        self.type = type
        self.load_images()
        self.frame = 0
        self.state = 'idle'
        self.health = 100 * (type + 1)
        self.attack_power = 10 * (type + 1)
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.build_behavior_tree()

    def draw(self):
        if math.cos(self.dir) < 0:
            Gorgon.image[self.type][self.state].clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        else:
            Gorgon.image[self.type][self.state].clip_draw(int(self.frame) * 128, 0, 128, 128, self.x, self.y, 128, 128)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 70, self.x + 40, self.y + 30

    def update(self):
        if self.state == 'die':
            div_num = 3
        else:
            div_num = 7
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % div_num
        self.bt.run()

    def handle_collision(self, group, other):
        if group == 'player:enemy':
            self.walk = False
            self.attack = True
        if group == 'attack:enemy':
            # 적 체력 감소
            self.health -= other.damage
            if self.health <= 0:
                self.die = True
                game_world.remove_object(self)
                # 아이템 드랍
                if random.random() < 0.5:  # 50% 확률로 아이템 드랍
                    dropped_item = item.Item(self.x + 10, self.y - 20, random.randint(0, 2))
                    game_world.add_object(dropped_item, 1)
                    game_world.add_collision_pair('player:item', None, dropped_item)

    def is_player_near(self, r = 0.5):
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            self.state = 'idle'
            return BehaviorTree.FAIL

    def move_to_player(self, r = 0.5):
        self.state = 'walk'
        self.move_little_to(share.player.x, share.player.y)
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_little_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def build_behavior_tree(self):
        c1 = Condition('Is player near', self.is_player_near, 7)
        a2 = Action('Move to', self.move_to_player, 2)
        root = Sequence('Move to target location', c1, a2)
        self.bt = BehaviorTree(root)


class Wizard:
    image = None
    def load_images(self):
        if Wizard.image == None:
            Wizard.image = {}
            for name in animation_names:
                Wizard.image[name] = load_image("sprite/Wizard_" + name + ".png")

    def __init__(self, x = 400, y = 300):
        self.x, self.y = x, y
        self.load_images()
        self.frame = 0
        self.state = 'idle'
        self.health = 50
        self.attack_power = 20
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.build_behavior_tree()

    def draw(self):
        if math.cos(self.dir) < 0:
            Wizard.image[self.state].clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', self.x, self.y, 200, 200)
        else:
            Wizard.image[self.state].clip_draw(int(self.frame) * 128, 0, 128, 128, self.x, self.y, 200, 200)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 100, self.x + 50, self.y + 10

    def update(self):
        if self.state == 'die' or self.state == 'walk':
            div_num = 6
        elif self.state == 'attack':
            div_num = 8
        else:
            div_num = 7
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % div_num
        self.bt.run()

    def handle_collision(self, group, other):
        if group == 'attack:enemy':
            # 적 체력 감소
            self.health -= other.damage
            if self.health <= 0:
                self.die = True
                game_world.remove_object(self)
                # 아이템 드랍
                if random.random() < 0.5:  # 50% 확률로 아이템 드랍
                    dropped_item = item.Item(self.x + 10, self.y - 20, random.randint(0, 2))
                    game_world.add_object(dropped_item, 1)
                    game_world.add_collision_pair('player:item', None, dropped_item)

    def is_player_near(self, r=0.5):
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            self.state = 'idle'
            return BehaviorTree.FAIL

    def move_to_player(self, r=0.5):
        self.state = 'walk'
        self.move_little_to(share.player.x, share.player.y)
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_little_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def build_behavior_tree(self):
        c1 = Condition('Is player near', self.is_player_near, 7)
        a2 = Action('Move to', self.move_to_player)
        root = Sequence('Move to target location', c1, a2)
        self.bt = BehaviorTree(root)