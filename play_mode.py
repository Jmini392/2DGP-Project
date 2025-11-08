# from pico2d import *
from background import Background
from player import *
from item import Item
import game_world
import framework
import random

player = None

def init():
    global player
    player = Player()
    game_world.add_object(player, 1)
    background = Background(2)
    game_world.add_object(background, 0)

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
    game_world.update()
    game_world.handle_collisions()

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