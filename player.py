from pico2d import *
from sdl2 import *
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
            self.player.frame = (self.player.frame + 1) % 5
            if self.player.frame == 4:
                self.player.state.handle_event(('IDLE_ENTER', None))
        elif self.special:
            self.player.frame = (self.player.frame + 1) % 6
            if self.player.frame == 5:
                self.player.state.handle_event(('IDLE_ENTER', None))


    def draw(self):
        if self.player.face_dir == 1:
            if self.special:
                self.player.special_attack_image.clip_draw(self.player.frame * 162, 0, 162, 162, self.player.x, self.player.y)
            else:
                self.player.attack_image.clip_draw(self.player.frame * 162, 0, 162, 162, self.player.x, self.player.y)
        else:
            if self.special:
                self.player.special_attack_image.clip_composite_draw(self.player.frame * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)
            else:
                self.player.attack_image.clip_composite_draw(self.player.frame * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)

class Walk:
    def __init__(self, player):
        self.player = player
        self.px, self.py = 0, 0

    def enter(self, e):
        if right_down(e):
            self.player.face_dir = 1
            self.player.mx += 1
            self.px += 1
        elif left_down(e):
            self.player.face_dir = -1
            self.player.mx -= 1
            self.px += 1
        elif up_down(e):
            self.player.my += 1
            self.py += 1
        elif down_down(e):
            self.player.my -= 1
            self.py += 1

    def exit(self, e):
        if self.px == 2:
            if right_up(e):
                self.px -= 1
                self.player.mx -= 1
                self.player.face_dir = -1
            elif left_up(e):
                self.px -= 1
                self.player.mx += 1
                self.player.face_dir = 1
        if self.py == 2:
            if up_up(e):
                self.py -= 1
                self.player.my -= 1
            elif down_up(e):
                self.py -= 1
                self.player.my += 1
        if self.px == 1:
            if right_up(e):
                self.px -= 1
                self.player.mx -= 1
            elif left_up(e):
                self.px -= 1
                self.player.mx += 1
        if self.py == 1:
            if up_up(e):
                self.py -= 1
                self.player.my -= 1
            if down_up(e):
                self.py -= 1
                self.player.my += 1

    def do(self):
        if self.player.mx == 0 and self.player.my == 0 and self.px == 0 and self.py == 0:
            self.player.state.handle_event(('IDLE_ENTER', None))
            return

        self.player.frame = (self.player.frame + 1) % 8
        if self.player.run:
            speed = 10
        else:
            speed = 5

        dx = 0
        dy = 0

        if self.player.mx == 1:
            dx = 1
            self.player.face_dir = 1
        elif self.player.mx == -1:
            dx = -1
            self.player.face_dir = -1
        if self.player.my == 1:
            dy = 1
        elif self.player.my == -1:
            dy = -1

        # 대각선 이동 시 속도 정규화
        if dx != 0 and dy != 0:
            import math
            normalize = math.sqrt(2)
            self.player.x += dx * speed / normalize
            self.player.y += dy * speed / normalize
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
                self.player.run_image.clip_draw(self.player.frame * 162, 0, 162, 162, self.player.x, self.player.y)
            else:
                self.player.walk_image.clip_draw(self.player.frame * 162, 0, 162, 162, self.player.x, self.player.y)
        else:
            if self.player.run:
                self.player.run_image.clip_composite_draw(self.player.frame * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)
            else:
                self.player.walk_image.clip_composite_draw(self.player.frame * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.mx = 0
        self.player.my = 0

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 4

    def draw(self):
        if self.player.face_dir == 1:
            self.player.idle_image.clip_draw(self.player.frame * 162, 0, 162, 162, self.player.x, self.player.y)
        else:
            self.player.idle_image.clip_composite_draw(self.player.frame * 162, 0, 162, 162, 0, 'h', self.player.x, self.player.y, 162, 162)


class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.mx, self.my = 0, 0
        self.frame = 0
        self.run = False
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
                    left_up : self.WALK, right_up : self.WALK,
                    up_up : self.WALK, down_up : self.WALK,
                    left_down: self.WALK, right_down: self.WALK,
                    up_down : self.WALK, down_down : self.WALK,
                    idle_enter : self.IDLE
                },
                self.ATTACK : { idle_enter : self.IDLE }
            })

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw()

    def handle_event(self, event):
        # 들어온 외부 키입력등을 상태 머신에 전달하기 위해서 튜플화 시킨후 전달
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LCTRL:
                self.run = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LCTRL:
                self.run = False
        self.state.handle_event(('INPUT', event))
