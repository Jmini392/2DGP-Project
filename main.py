from pico2d import *
from player import Player

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
    update_world()
    render_world()
    delay(0.01)

close_canvas()