from pico2d import *
import framework
import play_mode

def init():
    global image, arrow, y
    image = load_image('sprite/title.png')
    arrow = load_image('sprite/arrow.png')
    y = 375

def finish():
    global image, arrow
    del image
    del arrow

def handle_events():
    global y
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            if y == 275:
                y = 375
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            if y == 375:
                y = 275
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            y = 275
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            if y == 375:
                framework.change_mode(play_mode)
            elif y == 275:
                framework.quit()

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    arrow.draw(720, y, 70 ,60)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass