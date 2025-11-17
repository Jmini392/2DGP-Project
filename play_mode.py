from pico2d import *
from player import *
import game_world
import framework
import time
from background_manager import BackgroundManager
from stage_manager import StageManager
import shop_mode

player = None

# 충돌 쿨다운(초)
COLLISION_COOLDOWN = 0.5
LAST_COLLISION_TIME = 0.0

def init():
    global player, background_manager, stage_manager

    background_manager = BackgroundManager()
    game_world.add_object(background_manager, 0)

    stage_manager = StageManager()
    stage_manager.init_player()
    player = stage_manager.player
    stage_manager.load_stage(0)

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_v:
            if player.shopping:
                framework.push_mode(shop_mode)
                pass
        else:
            player.handle_event(event)

def update():
    global LAST_COLLISION_TIME
    game_world.update()
    stage_manager.update()

    old_stage = background_manager.current_stage
    old_background = background_manager.background
    # 플레이어 위치에 따라 스테이지 전환 체크
    background_manager.check_stage_transition(player)
    # 스테이지가 변경되었다면
    if old_stage != background_manager.current_stage:
        # 배경이 실제로 바뀐 경우에만 처리
        if old_background != background_manager.background:
            # game_world.remove_object(old_background)
            game_world.add_object(background_manager.background, 0)
        # 새로운 스테이지 객체 로드
        stage_manager.load_stage(background_manager.current_stage)

    now = time.time()
    if now - LAST_COLLISION_TIME >= COLLISION_COOLDOWN:
        game_world.handle_collisions()
        LAST_COLLISION_TIME = now

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass

def pause():
    pass

def resume():
    pass