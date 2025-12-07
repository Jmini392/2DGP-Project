from pico2d import *
import framework
import game_world
from shop import Stand
import share

stand = None

def init():
    global stand
    stand = Stand()
    game_world.add_object(stand, 2)
    share.bgm = load_music('sound/shop.mp3')
    share.bgm.repeat_play()

def finish():
    game_world.remove_object(stand)
    share.player.shopping = False
    game_world.add_object(share.player.ui, 2)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_v:
            framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            stand.arrow_move(-220)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            stand.arrow_move(220)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            stand.buy_item()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def update():
    game_world.update()

def pause():
    pass

def resume():
    pass