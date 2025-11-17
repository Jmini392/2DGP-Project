from pico2d import *
import framework
import game_world

def init():
    # global pannel
    # pannel = Pannel()
    # game_world.add_object(pannel, 2)
    pass

def finish():
    # game_world.remove_object(pannel)
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.type == SDLK_v:
            framework.pop_mode()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == 1:
            # play_mode.player.handle_shop_click(event.x, 600 - event.y)
            pass

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