from pico2d import *
from sdl2 import *

import framework
from state_machine import StateMachine

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z

def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

idle_enter = lambda e: e[0] == 'IDLE_ENTER'

#player frame
TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
# player speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Attack:
    def __init__(self, player):
        self.player = player
        self.normal = False
        self.special = False

    def enter(self, e):
        self.player.frame = 0
        if z_down(e):
            self.normal = True
        elif x_down(e):
            self.special = True

    def exit(self, e):
        self.normal = False
        self.special = False

    def do(self):
        if self.normal:
            self.player.frame = (self.player.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 5
            if self.player.frame > 4:
                self.player.state.handle_event(('IDLE_ENTER', None))
        elif self.special:
            self.player.frame = (self.player.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 6
            if self.player.frame > 5:
                self.player.state.handle_event(('IDLE_ENTER', None))


    def draw(self):
        if self.player.face_dir == 1:
            if self.special:
                self.player.special_attack_image.clip_draw(int(self.player.frame) * 162, 0, 162, 162, self.player.x, self.player.y)
            else:
                self.player.attack_image.clip_draw(int(self.player.frame) * 162, 0, 162, 162, self.player.x, self.player.y)
        else:
            if self.special:
                self.player.special_attack_image.clip_composite_draw(int(self.player.frame) * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)
            else:
                self.player.attack_image.clip_composite_draw(int(self.player.frame) * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)

class Walk:
    def __init__(self, player):
        self.player = player
        self.key_state = {'left': False, 'right': False, 'up': False, 'down': False}

    def enter(self, e):
        if left_down(e):
            self.key_state['left'] = True
        elif right_down(e):
            self.key_state['right'] = True
        elif up_down(e):
            self.key_state['up'] = True
        elif down_down(e):
            self.key_state['down'] = True

        if self.key_state['right']:
            self.player.face_dir = 1
        elif self.key_state['left']:
            self.player.face_dir = -1

    def exit(self, e):
        if left_up(e):
            self.key_state['left'] = False
        elif right_up(e):
            self.key_state['right'] = False
        elif up_up(e):
            self.key_state['up'] = False
        elif down_up(e):
            self.key_state['down'] = False

        if self.key_state['right']:
            self.player.face_dir = 1
        elif self.key_state['left']:
            self.player.face_dir = -1

    def do(self):
        if not any(self.key_state.values()):
            self.player.state.handle_event(('IDLE_ENTER', None))
            return

        dx = 0
        dy = 0

        if self.key_state['right']:
            dx += 1
        if self.key_state['left']:
            dx -= 1
        if self.key_state['up']:
            dy += 1
        if self.key_state['down']:
            dy -= 1

        self.player.frame = (self.player.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 8
        speed = RUN_SPEED_PPS * framework.frame_time
        if self.player.run:
            speed *= 2

        if dx != 0 and dy != 0:
            import math
            normalize = speed / math.sqrt(2)
            self.player.x += dx * normalize
            self.player.y += dy * normalize
        else:
            self.player.x += dx * speed
            self.player.y += dy * speed

        if self.player.x < 64:
            self.player.x = 64
        elif self.player.x > 800 - 64:
            self.player.x = 800 - 64
        if self.player.y < 64:
            self.player.y = 64
        elif self.player.y > 600 - 64:
            self.player.y = 600 - 64

    def draw(self):
        if self.player.face_dir == 1:
            if self.player.run:
                self.player.run_image.clip_draw(int(self.player.frame) * 162, 0, 162, 162, self.player.x, self.player.y)
            else:
                self.player.walk_image.clip_draw(int(self.player.frame) * 162, 0, 162, 162, self.player.x, self.player.y)
        else:
            if self.player.run:
                self.player.run_image.clip_composite_draw(int(self.player.frame) * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)
            else:
                self.player.walk_image.clip_composite_draw(int(self.player.frame) * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 4

    def draw(self):
        if self.player.face_dir == 1:
            self.player.idle_image.clip_draw(int(self.player.frame) * 162, 0, 162, 162, self.player.x, self.player.y)
        else:
            self.player.idle_image.clip_composite_draw(int(self.player.frame) * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)


class Player:
    def __init__(self):
        self.x, self.y = 100, 200
        self.face_dir = 1
        self.frame = 0
        self.run = False
        self.item = None
        self.inventory = {
            'speed': 10,
            'strong': 10,
            'health': 0
        }
        self.font = load_font('ENCR10B.TTF', 16)
        self.idle_image = load_image('sprite/idle.png')
        self.walk_image = load_image('sprite/Walk.png')
        self.run_image = load_image('sprite/Run.png')
        self.attack_image = load_image('sprite/Attack_1.png')
        self.special_attack_image = load_image('sprite/Attack_2.png')
        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.ATTACK = Attack(self)
        self.state = StateMachine (
            self.IDLE, {
                # 상태 규칙
                self.IDLE : {
                    left_down : self.WALK, right_down : self.WALK,
                    up_down : self.WALK, down_down : self.WALK,
                    z_down : self.ATTACK, x_down : self.ATTACK
                },
                self.WALK : {
                    left_down: self.WALK, right_down: self.WALK,
                    up_down: self.WALK, down_down: self.WALK,
                    left_up: self.WALK, right_up: self.WALK,
                    up_up: self.WALK, down_up: self.WALK,
                    idle_enter : self.IDLE
                },
                self.ATTACK : { idle_enter : self.IDLE }
            })

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw()
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - 40, self.y + 80, f'self.item:{self.item}, num:{self.inventory.get(self.item)}', (255, 255, 0))

    def get_bb(self):
        return self.x - 30, self.y - 70, self.x + 30, self.y + 70

    def handle_event(self, event):
        # 들어온 외부 키입력등을 상태 머신에 전달하기 위해서 튜플화 시킨후 전달
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LCTRL:
                self.run = True
            if event.key == SDLK_1:
                self.item = 'speed'
            elif event.key == SDLK_2:
                self.item = 'strong'
            elif event.key == SDLK_3:
                self.item = 'health'
            elif event.key == SDLK_c:
                if self.inventory.get(self.item) > 0:
                    self.inventory[self.item] -= 1
                else:
                    self.item = 'none'
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LCTRL:
                self.run = False
        self.state.handle_event(('INPUT', event))

    def handle_collision(self, group, other):
        if group == 'player:item':
            self.item = 'health'
            self.inventory[self.item] += 1