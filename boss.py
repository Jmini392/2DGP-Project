from pico2d import *
import framework
import game_world
import random
import share
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from game_world import remove_collision_object
from ui import EnemyUI

animation_names = ['walk', 'idle', 'die', 'hurt', 'attack1', 'attack2', 'attack3', 'attack4']

#boss speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#boss frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Boss:
    image = None
    def load_images(self):
        if Boss.image is None:
            Boss.image = {}
            for name in animation_names:
                Boss.image[name] = load_image("sprite/Boss_" + name + ".png")

    def __init__(self, x = 400, y = 300):
        self.x, self.y = x, y
        self.load_images()
        self.frame = 0
        self.action = 8
        self.state = 'idle'
        self.health = 500
        self.attack_num = 1
        self.power = 0
        self.stack = 0
        self.cool_time = 0.0
        self.sword = None
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.ui = EnemyUI(self, 4, 0)
        game_world.add_object(self.ui, 2)
        self.build_behavior_tree()

    def draw(self):
        if math.cos(self.dir) < 0:  # 왼쪽 바라볼 때
            Boss.image[self.state].clip_composite_draw(int(self.frame) * 254, 0, 254, 225, 0, 'h', self.x, self.y, 300, 300)
        else:  # 오른쪽 바라볼 때
            Boss.image[self.state].clip_draw(int(self.frame) * 254, 0, 254, 225, self.x, self.y, 300, 300)
        draw_rectangle(*self.get_bb())
        draw_circle(self.x, self.y, int(10 * PIXEL_PER_METER))

    def get_bb(self):
        if math.cos(self.dir) < 0:
            return self.x - 20, self.y - 90, self.x + 40, self.y + 20
        else:
            return self.x - 40, self.y - 90, self.x + 20, self.y + 20

    def update(self):
        if self.state == 'idle' or self.state == 'die' or self.state == 'hurt':
            div_num = 5
            if int(self.frame) == 4 and self.state == 'hurt':
                self.state = 'idle'
            if int(self.frame) == 4 and self.state == 'die':
                self.remove()
        elif self.state == 'walk' or self.state == 'attack2':
            div_num = 8
            if int(self.frame) == 7 and self.state == 'attack2':
                game_world.remove_object(self.sword)
                self.sword = None
                if self.stack >= 20:
                    self.attack_num = 4
                else:
                    self.attack_num = 1
                self.state = 'idle'
                self.frame = 0
        elif self.state == 'attack1':
            div_num = 9
            if int(self.frame) == 8:
                game_world.remove_object(self.sword)
                self.sword = None
                if self.stack >= 20:
                    self.attack_num = 4
                else:
                    self.attack_num = 2
                self.state = 'idle'
                self.frame = 0
        elif self.state == 'attack3':
            div_num = 10
            if int(self.frame) > 5:
                if math.cos(self.dir) < 0:
                    self.x -= 4
                else:
                    self.x += 4
            if int(self.frame) == 9:
                game_world.remove_object(self.sword)
                self.sword = None
                self.state = 'idle'
                self.attack_num = 1
                self.frame = 0
        elif self.state == 'attack4':
            div_num = 30
            if int(self.frame) == 29:
                game_world.remove_object(self.sword)
                self.sword = None
                self.attack_num = 1
                self.frame = 0
                self.stack = 0
                self.state = 'idle'
        self.frame = (self.frame + ACTION_PER_TIME * self.action * framework.frame_time) % div_num
        self.bt.run()
        if self.cool_time > 0.0:
            self.cool_time -= framework.frame_time

    def remove(self):
        game_world.remove_object(self)
        game_world.remove_object(self.ui)

    def handle_collision(self, group, other):
        if not self.state == 'die' and not self.state == 'hurt':
            if group == 'attack:enemy':
                self.frame = 0
                self.action = 5
                self.state = 'hurt'
                if self.sword is not None:
                    game_world.remove_object(self.sword)
                    self.sword = None
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
        if self.state == 'die' or self.state == 'hurt':
            return BehaviorTree.FAIL
        else:
            self.action = 8
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
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def cooldown(self, r = 1):
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            return BehaviorTree.FAIL
        elif self.cool_time <= 0.0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def dash_attack(self):
        self.state = 'attack3'
        self.sword = Sword(self, self.power)
        game_world.add_object(self.sword, 1)
        game_world.add_collision_pair('player:enemy', None, self.sword)
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.cool_time = 4.0
        self.frame = 0
        self.power = 40
        self.stack += 1
        return BehaviorTree.SUCCESS

    def move_to_player(self, r = 0.5):
        self.state = 'walk'
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            self.state = 'attack' + str(self.attack_num)
            self.sword = Sword(self, self.power)
            game_world.add_object(self.sword, 1)
            game_world.add_collision_pair('player:enemy', None, self.sword)
            if self.attack_num == 4:
                self.stack = 0
                self.frame = 0
                self.power = 50
            else:
                self.stack += 1
                self.frame = 0
                self.power = 30
            return BehaviorTree.SUCCESS
        else:
            self.move_little_to(share.player.x, share.player.y + 40, 2)
            return BehaviorTree.RUNNING

    def attacking(self):
        if self.state == 'attack1' or self.state == 'attack2' or self.state == 'attack3' or self.state == 'attack4':
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        c1 = Condition('Not move', self.if_hurt)

        c = Condition('cooltime', self.cooldown, 10)
        a = Action('attack3', self.dash_attack)
        seq = Sequence('Move to player seq', c, a)

        a1 = Action('Move to player', self.move_to_player, 2)
        Move = Selector('Move to player', seq, a1)

        c3 = Condition('Attack action', self.attacking)

        s = Sequence('Follow_and_attack', c3, Move)

        root = Sequence("", c1, s)
        self.bt = BehaviorTree(root)

class Sword:
    def __init__(self, boss, damage = 30):
        self.boss = boss
        self.face_dir = boss.dir
        self.x, self.y = boss.x, boss.y
        self.state = 'attack'
        self.power = self.boss.power

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x, self.y = self.boss.x, self.boss.y

    def get_bb(self):
        if self.boss.state == 'attack1':
            if math.cos(self.face_dir) < 0:
                return self.x - 80, self.y - 40, self.x - 20, self.y + 20
            else:
                return self.x + 20, self.y - 40, self.x + 80, self.y + 20
        elif self.boss.state == 'attack2':
            if math.cos(self.face_dir) < 0:
                return self.x - 80, self.y - 60, self.x - 20, self.y + 30
            else:
                return self.x + 20, self.y - 60, self.x + 80, self.y + 30
        elif self.boss.state == 'attack3':
            if math.cos(self.face_dir) < 0:
                return self.x - 100, self.y - 80, self.x - 20, self.y + 40
            else:
                return self.x + 20, self.y - 80, self.x + 100, self.y + 40
        else:
            if math.cos(self.face_dir) < 0:
                return self.x - 120, self.y - 100, self.x - 20, self.y + 50
            else:
                return self.x + 20, self.y - 100, self.x + 120, self.y + 50

    def handle_collision(self, group, other):
        pass