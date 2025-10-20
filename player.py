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

class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if right_down(e):
            self.player.face_dir = 1
            self.player.dir = 1
        elif left_down(e):
            self.player.face_dir = -1
            self.player.dir = -1
        elif up_down(e):
            self.player.dir = 2
        elif down_down(e):
            self.player.dir = -2

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 8
        if self.player.dir == 1 or self.player.dir == -1:
            self.player.x += self.player.dir * 5
            if self.player.x < 64:
                self.player.x = 64
            elif self.player.x > 800 - 64:
                self.player.x = 800 - 64
        elif self.player.dir == 2 or self.player.dir == -2:
            self.player.y += self.player.dir / 2 * 5
            if self.player.y < 64:
                self.player.y = 64
            elif self.player.y > 600 - 64:
                self.player.y = 600 - 64

    def draw(self):
        if self.player.face_dir == 1:
            self.player.walk_image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y)
        else:
            self.player.walk_image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 128, 128)


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 6

    def draw(self):
        if self.player.face_dir == 1:
            self.player.idle_image.clip_draw(self.player.frame * 128, 0, 128, 128, self.player.x, self.player.y)
        else:
            self.player.idle_image.clip_composite_draw(self.player.frame * 128, 0, 128, 128, 0, 'h', self.player.x, self.player.y, 128, 128)


class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.dir = 0
        self.frame = 0
        self.idle_image = load_image('idle.png')
        self.walk_image = load_image('Walk.png')
        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.state = StateMachine (
            self.IDLE, {
                # 상태 규칙
                self.IDLE : {
                    left_down : self.WALK,
                    right_down : self.WALK,
                    up_down : self.WALK,
                    down_down : self.WALK
                },
                self.WALK : {
                    left_up : self.IDLE,
                    right_up : self.IDLE,
                    up_up : self.IDLE,
                    down_up : self.IDLE
                }
            })

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw()

    def handle_event(self, event):
        # 들어온 외부 키입력등을 상태 머신에 전달하기 위해서 튜플화 시킨후 전달
        self.state.handle_event(('INPUT', event))
