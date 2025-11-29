from pico2d import *
import framework
import title_mode

def init():
    global image
    global logo_start_time
    image = load_image('sprite/tuk_credit.png')
    logo_start_time = get_time()

def finish():
    global image
    del image

def handle_events():
    pass

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    update_canvas()

def update():
    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        framework.change_mode(title_mode)

def pause():
    pass

def resume():
    pass