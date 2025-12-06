from pico2d import *
import framework
import play_mode
import share

def init():
    global image, arrow, y, blink_timer, show_arrow
    image = load_image('sprite/title.png')
    arrow = load_image('sprite/arrow.png')
    y = 375
    blink_timer = 0.0
    show_arrow = True

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if y == 375:
                framework.change_mode(play_mode)
            elif y == 275:
                framework.quit()

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    if show_arrow:
        arrow.draw(720, y, 70, 60)
    update_canvas()

def update():
    global blink_timer, show_arrow
    blink_timer += framework.frame_time
    if blink_timer >= 0.3:
        blink_timer = 0.0
        show_arrow = not show_arrow

def pause():
    pass

def resume():
    pass