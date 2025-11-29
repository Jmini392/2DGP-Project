from pico2d import *
import framework
import game_world
import random
import item
import share
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from ui import EnemyUI

animation_names = ['idle', 'attack', 'die', 'hurt']

#wizard fire speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#wizard frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Wizard:
    image = None
    def load_images(self):
        if Wizard.image == None:
            Wizard.image = {}
            for name in animation_names:
                Wizard.image[name] = load_image("sprite/Wizard_" + name + ".png")

    def __init__(self, x = 400, y = 300, num = 0):
        self.x, self.y = x, y
        self.tx, self.ty = 0, 0
        self.load_images()
        self.frame = 0
        self.state = 'idle'
        self.health = 50
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.ui = EnemyUI(self, 3, num)
        game_world.add_object(self.ui, 2)
        self.fireBall_cooldown = 0.0
        self.is_attacked = False
        self.build_behavior_tree()

    def draw(self):
        if math.cos(self.dir) < 0:
            Wizard.image[self.state].clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', self.x, self.y, 200, 200)
        else:
            Wizard.image[self.state].clip_draw(int(self.frame) * 128, 0, 128, 128, self.x, self.y, 200, 200)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if math.cos(self.dir) < 0:
            return self.x - 10, self.y - 100, self.x + 50, self.y + 10
        else:
            return self.x - 50, self.y - 100, self.x + 10, self.y + 10

    def update(self):
        if self.state == 'die' or self.state == 'walk':
            div_num = 6
            if int(self.frame) == 5 and self.state == 'die':
                self.remove()
        elif self.state == 'attack':
            div_num = 8
            if int(self.frame) == 7:
                if self.fireBall_cooldown <= 0.0:
                    fire_ball = FireBall(self.x, self.y, self.dir)
                    game_world.add_object(fire_ball, 1)
                    game_world.add_collision_pair('player:enemy', None, fire_ball)
                    game_world.add_collision_pair('attack:enemy', None, fire_ball)
                    self.fireBall_cooldown = 2.0
                    self.state = 'idle'
        else:
            div_num = 7
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % div_num
        self.bt.run()
        if self.fireBall_cooldown > 0.0:
            self.fireBall_cooldown -= framework.frame_time

    def handle_collision(self, group, other):
        if group == 'attack:enemy':
            # 적 체력 감소
            self.health -= other.damage
            self.is_attacked = True
            if self.health <= 0:
                self.health = 0
                self.state = 'die'
                self.frame = 0

    def remove(self):
        game_world.remove_object(self)
        game_world.remove_object(self.ui)
        # 아이템 드랍
        if random.random() < 0.5:  # 50% 확률로 아이템 드랍
            dropped_item = item.Item(self.x + 10, self.y - 20, random.randint(0, 2))
            game_world.add_object(dropped_item, 1)
            game_world.add_collision_pair('player:item', None, dropped_item)

    def if_not_dead(self):
        if self.health > 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def find_player(self):
        self.tx, self.ty = share.player.x, share.player.y
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        return BehaviorTree.SUCCESS

    def attack_player(self):
        self.state = 'attack'
        return BehaviorTree.SUCCESS

    def if_attack_cooldown(self):
        if self.fireBall_cooldown <= 0.0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def if_attacked(self):
        if self.is_attacked:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def get_random_location(self):
        self.tx = random.randint(100, 1200)
        self.ty = random.randint(100, 500)
        return BehaviorTree.SUCCESS

    def teleport(self):
        self.x , self.y = self.tx, self.ty
        self.is_attacked = False
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        c1 = Condition('Not dead', self.if_not_dead)
        a1 = Action('Find player', self.find_player)
        a2 = Action('Attack',self.attack_player)
        c2 = Condition('Attack cooldown', self.if_attack_cooldown)
        attack = Sequence('Attack', a1, c2, a2)
        a3 = Action('Random',self.get_random_location)
        a4 = Action('Move to target location',self.teleport)
        move = Sequence('Move', a3, a4)
        c3 = Condition('Player near', self.if_attacked)
        run = Sequence('Run from player', c3, move)
        attack_or_move = Selector('Attack_or_move', run, attack)
        wizard = Sequence('Wizard', c1, attack_or_move)
        root = wizard
        self.bt = BehaviorTree(root)

class FireBall:
    image = None
    def __init__(self, x, y, dir):
        self.x, self.y = x, y - 30
        self.dir = dir
        self.frame = 0
        self.power = 20
        if FireBall.image is None:
            FireBall.image = load_image('sprite/wizard_effect.png')

    def draw(self):
        if math.cos(self.dir) < 0:
            FireBall.image.clip_composite_draw(int(self.frame) * 64, 0, 64, 64, 0, 'h', self.x, self.y, 100, 100)
        else:
            FireBall.image.clip_draw(int(self.frame) * 64, 0, 64, 64, self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if math.cos(self.dir) < 0:
            return self.x - 50, self.y - 20, self.x, self.y + 20
        else:
            return self.x, self.y - 20, self.x + 50, self.y + 20

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 4
        distance = RUN_SPEED_PPS * framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def handle_collision(self, group, other):
        if group == 'player:enemy':
            game_world.remove_object(self)
        elif group == 'attack:enemy':
            game_world.remove_object(self)