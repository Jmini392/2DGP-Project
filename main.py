from pico2d import *
from player import Player

# 이벤트 처리
def handle_events():
    global running
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# 월드 초기화
def reset_world():
    global world
    world = []
    player = Player()
    world.append(player)

# 월드 업데이트
def update_world():
    for o in world:
        o.update()


# 월드 랜더링
def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True
open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)

close_canvas()