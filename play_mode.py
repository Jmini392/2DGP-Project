from pico2d import *
from player import *
import game_world
import framework

player = None

def init():
    global running
    running = True
    global player
    player = Player()
    game_world.add_object(player, 1)

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