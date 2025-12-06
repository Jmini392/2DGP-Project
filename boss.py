from pico2d import *
import framework
import game_world
import random
import share
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
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
        self.sound = load_wav('sound/boss_attack2.wav')
        self.sound.set_volume(90)
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.ui = EnemyUI(self, 4, 0)
        game_world.add_object(self.ui, 2)
        self.build_behavior_tree()

    def draw(self):
        if math.cos(self.dir) < 0:  # 왼쪽 바라볼 때
            Boss.image[self.state].clip_composite_draw(int(self.frame) * 254, 0, 254, 225, 0, 'h', self.x, self.y, 300, 300)
        else:  # 오른쪽 바라볼 때
            Boss.image[self.state].clip_draw(int(self.frame) * 254, 0, 254, 225, self.x, self.y, 300, 300)

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
                self.action = 8
            if int(self.frame) == 4 and self.state == 'die':
                self.remove()
        elif self.state == 'walk' or self.state == 'attack2':
            div_num = 8
            if self.state == 'attack2':
                if int(self.frame) == 2:
                    self.sound.play()
                if int(self.frame) == 7:
                    if self.sword is not None:
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
            if int(self.frame) == 2:
                self.sound.play()
            if int(self.frame) == 8:
                if self.sword is not None:
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
            if int(self.frame) == 3:
                self.sound.play()
            if int(self.frame) > 5:
                if math.cos(self.dir) < 0:
                    self.x -= 30 * PIXEL_PER_METER * framework.frame_time
                else:
                    self.x += 30 * PIXEL_PER_METER * framework.frame_time
            if int(self.frame) == 9:
                if self.sword is not None:
                    game_world.remove_object(self.sword)
                    self.sword = None
                self.attack_num = 1
                self.state = 'idle'
                self.frame = 0
        elif self.state == 'attack4':
            div_num = 30
            if int(self.frame) in [2, 10, 17, 20]:
                self.sound.play()
            if int(self.frame) == 29:
                if self.sword is not None:
                    game_world.remove_object(self.sword)
                    self.sword = None
                self.attack_num = 1
                self.frame = 0
                self.state = 'idle'
        self.frame = (self.frame + ACTION_PER_TIME * self.action * framework.frame_time) % div_num
        self.bt.run()
        if self.cool_time > 0.0:
            self.cool_time -= framework.frame_time

    def remove(self):
        game_world.remove_object(self)
        game_world.remove_object(self.ui)
        share.player.win = True
        share.bgm = load_music('sound/ending.mp3')
        share.bgm.play()

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
                    self.sound = load_wav('sound/boss_death.wav')
                    self.sound.play()
                    self.health = 0
                    self.state = 'die'

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

    def if_cooldown(self, r = 1):
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            return BehaviorTree.FAIL
        elif self.cool_time <= 0.0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def if_check_busy(self):
        if self.state in ['die', 'hurt', 'attack1', 'attack2', 'attack3', 'attack4']:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def if_stack_full(self):
        if self.stack >= 20:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def do_attack(self):
        self.state = 'attack' + str(self.attack_num)
        self.sound = load_wav('sound/boss_attack2.wav')
        self.stack += 1
        self.frame = 0
        self.power = 30
        self.sword = Sword(self, self.power)
        game_world.add_object(self.sword, 1)
        game_world.add_collision_pair('player:enemy', None, self.sword)
        return BehaviorTree.SUCCESS

    def do_dash_attack(self):
        self.state = 'attack3'
        self.sound = load_wav('sound/boss_attack1.wav')
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.stack += 1
        self.frame = 0
        self.power = 40
        self.cool_time = 4.0
        self.sword = Sword(self, self.power)
        game_world.add_object(self.sword, 1)
        game_world.add_collision_pair('player:enemy', None, self.sword)
        return BehaviorTree.SUCCESS

    def do_ultimate_attack(self):
        self.state = 'attack4'
        self.sound = load_wav('sound/boss_attack2.wav')
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.stack = 0
        self.frame = 0
        self.power = 60
        self.sword = Sword(self, self.power)
        game_world.add_object(self.sword, 1)
        game_world.add_collision_pair('player:enemy', None, self.sword)
        return BehaviorTree.SUCCESS

    def move_to_player(self, r = 0.5):
        self.state = 'walk'
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            self.move_little_to(share.player.x, share.player.y + 40, 2)
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c_busy = Condition('동작 중인지 확인', self.if_check_busy)

        c_stack_full = Condition('스택 확인', self.if_stack_full)
        a_ultimate = Action('궁극기 발동', self.do_ultimate_attack)
        seq_ultimate = Sequence('광폭화 패턴', c_stack_full, a_ultimate)

        c_dash_cond = Condition('대시 조건 확인', self.if_cooldown, 4)
        a_dash = Action('대시 공격', self.do_dash_attack)
        seq_dash = Sequence('대시 공격 시퀀스', c_dash_cond, a_dash)

        c_near = Condition('근접 거리 확인', self.if_player_near, 2)
        a_move = Action('플레이어 다가가기', self.move_to_player, 2)
        a_attack = Action('근접 공격', self.do_attack)
        seq_attack = Sequence('근접 공격 시퀀스', c_near, a_move, a_attack)

        a_chase = Action('플레이어 추격', self.move_to_player, 2)

        sel_combat = Selector('전투 패턴 선택', seq_ultimate, seq_dash, seq_attack, a_chase)

        root = Selector('보스 AI 루트', c_busy, sel_combat)

        self.bt = BehaviorTree(root)

class Sword:
    def __init__(self, boss, damage = 30):
        self.boss = boss
        self.face_dir = boss.dir
        self.x, self.y = boss.x, boss.y
        self.state = 'attack'
        self.power = self.boss.power

    def draw(self):
        pass

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
        elif self.boss.state == 'attack4':
            if math.cos(self.face_dir) < 0:
                return self.x - 120, self.y - 100, self.x - 20, self.y + 50
            else:
                return self.x + 20, self.y - 100, self.x + 120, self.y + 50
        else:
            return 0, 0, 0, 0

    def handle_collision(self, group, other):
        pass