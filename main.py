from pico2d import *

import game_world
from player import Player
from game_world import *

# 이벤트 처리
def handle_events():
    global running
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)

# 월드 초기화
def reset_world():
    global player
    player = Player()
    game_world.add_object(player, 1)

# 월드 업데이트
def update_world():
    game_world.update()

# 월드 랜더링
def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


running = True
open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()