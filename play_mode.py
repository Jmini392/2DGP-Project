# from pico2d import *
from background import Background
from player import *
from enemy import Enemy
import game_world
import framework
import random
import time

player = None

# 충돌 쿨다운(초)
COLLISION_COOLDOWN = 0.5
LAST_COLLISION_TIME = 0.0

def init():
    global player
    player = Player()
    game_world.add_object(player, 1)
    background = Background(2)
    game_world.add_object(background, 0)
    enemy = Enemy(400, 200, 'Gorgon', 100, 10)
    game_world.add_object(enemy, 1)
    game_world.add_collision_pair( 'player:enemy', player, None)
    game_world.add_collision_pair('player:enemy', None, enemy)
    game_world.add_collision_pair( 'player:item', player, None)

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        else:
            player.handle_event(event)

def update():
    global LAST_COLLISION_TIME
    game_world.update()
    now = time.time()
    if now - LAST_COLLISION_TIME >= COLLISION_COOLDOWN:
        game_world.handle_collisions()
        LAST_COLLISION_TIME = now

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass

def pause():
    pass

def resume():
    pass