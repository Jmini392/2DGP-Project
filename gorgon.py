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

    def __init__(self, x = 400, y = 300, style = 0, num = 0):
        self.x, self.y = x, y
        self.type = style + 1
        self.load_images()
        self.frame = 0
        self.action = 7
        self.state = 'idle'
        self.health = 100 * self.type
        self.power = 0
        if self.type == 1:
            self.attack_range = 0.5
        elif self.type == 2:
            self.attack_range = 0.68
        else:
            self.attack_range = 4.5
        self.sound = load_wav('sound/gorgon_attack.wav')
        self.sound.set_volume(50)
        self.check_time = 0.0
        self.find = False
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.ui = EnemyUI(self, self.type - 1, num)
        game_world.add_object(self.ui, 2)
        self.build_behavior_tree()

    def draw(self):
        if math.cos(self.dir) < 0: # 왼쪽 바라볼 때
            Gorgon.image[self.type - 1][self.state].clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h',
                                                            self.x, self.y, 128 + (self.type * 50), 128 + (self.type * 50))
        else: # 오른쪽 바라볼 때
            Gorgon.image[self.type - 1][self.state].clip_draw(int(self.frame) * 128, 0, 128, 128,
                                                            self.x, self.y, 128 + (self.type * 50), 128 + (self.type * 50))
        draw_rectangle(*self.get_bb())
        draw_circle(self.x, self.y, int(PIXEL_PER_METER * (7 + (3 * self.type))))
        draw_circle(self.x, self.y, int(PIXEL_PER_METER * (self.attack_range + (1 * self.type))), 255,0,255)

    def get_bb(self):
        if self.type == 1:
            if self.state == 'hurt':
                if math.cos(self.dir) < 0:
                    return self.x, self.y - 90, self.x + 50, self.y + 30
                else:
                    return self.x - 50, self.y - 90, self.x, self.y + 30
            elif self.state == 'walk':
                if math.cos(self.dir) < 0:
                    return self.x - 70, self.y - 90, self.x - 20, self.y + 30
                else:
                    return self.x + 20, self.y - 90, self.x + 70, self.y + 30
            else:
                if math.cos(self.dir) < 0:
                    return self.x - 20, self.y - 90, self.x + 30, self.y + 30
                else:
                    return self.x - 30, self.y - 90, self.x + 20, self.y + 30
        elif self.type == 2:
            if self.state == 'hurt':
                if math.cos(self.dir) < 0:
                    return self.x, self.y - 120, self.x + 60, self.y + 40
                else:
                    return self.x - 60, self.y - 120, self.x, self.y + 40
            elif self.state == 'walk':
                if math.cos(self.dir) < 0:
                    return self.x - 90, self.y - 120, self.x - 30, self.y + 40
                else:
                    return self.x + 30, self.y - 120, self.x + 90, self.y + 40
            else:
                if math.cos(self.dir) < 0:
                    return self.x - 50, self.y - 120, self.x + 10, self.y + 40
                else:
                    return self.x - 10, self.y - 120, self.x + 50, self.y + 40
        else:
            if self.state == 'hurt':
                if math.cos(self.dir) < 0:
                    return self.x, self.y - 140, self.x + 70, self.y + 50
                else:
                    return self.x - 70, self.y - 140, self.x, self.y + 50
            elif self.state == 'walk':
                if math.cos(self.dir) < 0:
                    return self.x - 110, self.y - 140, self.x - 40, self.y + 50
                else:
                    return self.x + 40, self.y - 140, self.x + 110, self.y + 50
            if math.cos(self.dir) < 0:
                return self.x - 40, self.y - 140, self.x + 30, self.y + 50
            else:
                return self.x - 30, self.y - 140, self.x + 40, self.y + 50

    def update(self):
        if self.state == 'die' or self.state == 'hurt':
            div_num = 3
            if int(self.frame) == 2 and self.state == 'hurt':
                self.state = 'idle'
                self.action = 7
            elif int(self.frame) == 2 and self.state == 'die':
                self.remove()
        else:
            if self.type == 3 and self.state == 'attack':
                div_num = 9
                if int (self.frame) > 3:
                    if math.cos(self.dir) < 0:
                        self.x -= 20 * PIXEL_PER_METER * framework.frame_time
                    else:
                        self.x += 20 * PIXEL_PER_METER * framework.frame_time
                if int(self.frame) == 8:
                    self.state = 'idle'
                    self.power = 0
            else:
                div_num = 7
                if int(self.frame) == 6 and self.state == 'attack':
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
        if not self.state == 'die' and not self.state == 'hurt':
            if group == 'attack:enemy':
                self.action = 3
                self.frame = 0
                self.state = 'hurt'
                self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
                if math.cos(self.dir) < 0:
                    self.x += 20 * self.type
                else :
                    self.x -= 20 * self.type
                self.health -= other.damage
                if self.health <= 0:
                    self.health = 0
                    self.state = 'die'
                    self.sound = load_wav('sound/gorgon_death.wav')
                    self.sound.set_volume(50)
                    self.sound.play()
                    share.player.inventory['money'] += 100 * self.type

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_little_to(self, tx, ty, speed = 1.0):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * framework.frame_time * speed
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def if_not_busy(self):
        if self.state in ['hurt', 'die', 'attack'] or share.player.die:
            return BehaviorTree.FAIL
        else:
            self.action = 7
            return BehaviorTree.SUCCESS

    def if_time_over(self):
        if self.check_time <= 0.0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def if_cooldown_active(self):
        if self.check_time > 0.0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def if_player_in_attack_range(self, r):
        r_val = r + (1 * self.type)
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r_val):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def if_player_near(self, r = 0.5):
        if self.find:
            return BehaviorTree.SUCCESS
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r):
            self.find = True
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def if_chase_mode_active(self, r):
        if self.find:
            return BehaviorTree.SUCCESS
        r_val = r + (3 * self.type)
        if self.distance_less_than(share.player.x, share.player.y, self.x, self.y, r_val):
            self.find = True
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def do_idle(self):
        self.state = 'idle'
        return BehaviorTree.SUCCESS

    def do_attack(self):
        self.state = 'attack'
        self.sound.play()
        self.dir = math.atan2(share.player.y - self.y, share.player.x - self.x)
        self.power = 10 + self.type * 5
        self.check_time = 3.0
        self.frame = 0
        return BehaviorTree.SUCCESS

    def move_to_player(self, r=2.5):
        self.state = 'walk'
        self.move_little_to(share.player.x, share.player.y + 25 * self.type, 2.0)
        return BehaviorTree.RUNNING

    def get_random_location(self):
        self.tx = random.randint(int(self.x - 100), int(self.x + 100))
        self.ty = random.randint(int(self.y - 10), int(self.y + 10))
        return BehaviorTree.SUCCESS

    def move_to(self, r = 0.5):
        self.state = 'walk'
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            self.state = 'idle'
            self.check_time = 2.0
            return BehaviorTree.SUCCESS
        else:
            self.move_little_to(self.tx, self.ty)
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('Not Busy', self.if_not_busy)

        c2 = Condition('Persistent Chase Active', self.if_chase_mode_active, 7.0)

        c3 = Condition('Cooldown Active', self.if_cooldown_active)
        c4 = Condition('In Attack Range', self.if_player_in_attack_range, self.attack_range)
        a1 = Action('Do Idle', self.do_idle)
        idle_in_range = Sequence('Idle in Range', c4, a1)

        a2 = Action('Move to Player', self.move_to_player)
        cooldown_selector = Selector('Cool Behavior', idle_in_range, a2)

        cooldown_manager = Sequence('Cooldown Manager', c3, cooldown_selector)

        c5 = Condition('Time Over', self.if_time_over)
        a3 = Action('Attack', self.do_attack)
        attack_if_ready = Sequence('Attack If Ready', c4, c5, a3)

        combat_selector = Selector('Combat Selector', attack_if_ready, a2, a1)

        chase_logic = Selector('Chase Logic', cooldown_manager, combat_selector)

        chase_and_combat = Sequence('Chase and Combat', c2, chase_logic)

        c6 = Condition('Wait Over', self.if_time_over)
        a4 = Action('Random Loc', self.get_random_location)
        a5 = Action('Move To', self.move_to)
        patrol = Sequence('Patrol', c6, a4, a5)

        s = Selector('Main Selector', chase_and_combat, patrol)
        root = Sequence('Root', c1, s)
        self.bt = BehaviorTree(root)