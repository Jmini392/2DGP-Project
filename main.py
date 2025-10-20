from pico2d import *
import player

# 월드 초기화
def reset_world():
    pass

# 월드 업데이트
def update_world():
    pass

# 월드 랜더링
def render_world():
    pass


running = True
open_canvas()
reset_world()
# game loop
while running:
    update_world()
    render_world()
    delay(0.01)

close_canvas()