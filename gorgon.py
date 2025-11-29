from pico2d import *
import framework
import game_world
import random
import item
import share
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from ui import EnemyUI

animation_names = ['walk', 'idle', 'attack', 'die', 'hurt']

#gorgon speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#gorgon frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Gorgon:
    image = None
    def load_images(self):
        if Gorgon.image == None:
            Gorgon.image = {}
            for i in range(3):
                Gorgon.image[i] = {}
                for name in animation_names:
                    Gorgon.image[i][name] = load_image("sprite/Gorgon" + str(i + 1) + "_" + name + ".png")

    def __init__(self, x = 400, y = 300, type = 0, num = 0):
        self.x, self.y = x, y
        self.type = type
        self.load_images()
        self.frame = 0
        self.action = 7
        self.state = 'idle'
        self.health = 100 * (type + 1)
        self.power = 0

        self.check_time = 0.0
        self.find = False

        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.ui = EnemyUI(self, self.type, num)
        game_world.add_object(self.ui, 2)

        self.build_behavior_tree()

    def draw(self):
        if math.cos(self.dir) < 0: # 왼쪽 바라볼 때
            Gorgon.image[self.type][self.state].clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128 * (self.type + 1), 128 * (self.type + 1))
        else: # 오른쪽 바라볼 때
            Gorgon.image[self.type][self.state].clip_draw(int(self.frame) * 128, 0, 128, 128, self.x, self.y, 128 * (self.type + 1), 128 * (self.type + 1))
        draw_rectangle(*self.get_bb())
        draw_circle(self.x, self.y, int((7 + 3 * self.type) * PIXEL_PER_METER))
        draw_circle(self.x, self.y, int((2 + 1 * self.type) * PIXEL_PER_METER), 255,0,255)

    def get_bb(self):
        return self.x - 40 * (self.type + 1), self.y - 70* (self.type + 1), self.x + 40* (self.type + 1), self.y + 40* (self.type + 1)

    def update(self):
        if self.state == 'die' or self.state == 'hurt':
            div_num = 3
            if int(self.frame) == 2 and self.state == 'hurt':
                self.state = 'idle'
                self.action = 7
            elif int(self.frame) == 2 and self.state == 'die':
                self.remove()
        else:
            div_num = 7
            if self.state == 'attack' and int(self.frame) == 6:
                self.state = 'idle'
                self.power = 0
        self.frame = (self.frame + ACTION_PER_TIME * self.action * framework.frame_time) % div_num
        self.bt.run()
        if self.check_time > 0.0:
            self.check_time -= framework.frame_time

    def remove(self):
        game_world.remove_object(self)
        game_world.remove_object(self.ui)
        # 아이템 드랍
        if random.random() < 0.5:  # 50% 확률로 아이템 드랍
            dropped_item = item.Item(self.x + 10, self.y - 20, random.randint(0, 2))
            game_world.add_object(dropped_item, 1)
            game_world.add_collision_pair('player:item', None, dropped_item)

    def handle_collision(self, group, other):
        if not self.state == 'die':
            if group == 'attack:enemy':
                self.action = 3
                self.frame = 0
                self.state = 'hurt'
                self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
                if math.cos(self.dir) < 0:
                    self.x += 15
                else :
                    self.x -= 15
                self.health -= other.damage
                if self.health <= 0:
                    self.health = 0
                    self.state = 'die'

    def if_hurt(self):
        if self.state == 'hurt' or self.state == 'die':
            return BehaviorTree.FAIL
        else:
            self.action = 7
            return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_little_to(self, tx, ty, speed = 1.0):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * framework.frame_time * speed
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def if_player_near(self, r = 0.5):
        if self.find:
            return BehaviorTree.SUCCESS
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            self.find = True
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_player(self, r = 0.5):
        self.state = 'walk'
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            if self.check_time <= 0.0:
                self.state = 'attack'
                self.power = 10 + self.type * 5
                self.check_time = 3.0
                return BehaviorTree.SUCCESS
            else:
                self.state = 'idle'
                return BehaviorTree.SUCCESS
        else:
            self.move_little_to(share.player.x, share.player.y, 1.5)
            return BehaviorTree.RUNNING

    def attack_player(self):
        if self.state != 'attack':
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def check_time_over(self):
        if self.find:
            return BehaviorTree.FAIL
        if self.check_time <= 0.0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def get_random_location(self):
        self.tx = random.randint(int(self.x - 100), int(self.x + 100))
        self.ty = random.randint(int(self.y - 10), int(self.y + 10))
        return BehaviorTree.SUCCESS

    def move_to(self, r = 0.5):
        self.state = 'walk'
        self.move_little_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            self.state = 'idle'
            self.check_time = 2.0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        # 시간이 흐르고 있으면 멈춤, 플레이어를 발견하면 따라가서 공격, 멀어지면 랜덤 이동
        c1 = Condition('Not move', self.if_hurt)

        c2 = Condition('Find player', self.if_player_near, 7 + 3 * self.type)
        a1 = Action('Move to player', self.move_to_player, 2 + 1 * self.type)
        a2 = Action('Attack', self.attack_player)
        follow_and_attack = Sequence('Follow_and_attack', c2, a2, a1)

        c3 = Condition('Time check', self.check_time_over)
        a3 = Action('Random walk', self.get_random_location)
        a4 = Action('Move to', self.move_to)
        random_walk = Sequence('random_walk', c3, a3, a4)

        s = Selector("", follow_and_attack, random_walk)
        root = Sequence("", c1, s)
        self.bt = BehaviorTree(root)