from pico2d import *
import framework
import game_world
from shop import Stand
import item

stand = None

def init():
    global stand
    stand = Stand()
    game_world.add_object(stand, 2)

def shop_item_click(x, y):
    # 상점 아이템 클릭 처리 로직 구현
    pass

def finish():
    game_world.remove_object(stand)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_v:
            framework.pop_mode()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == 1:
            shop_item_click(event.x, event.y)

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