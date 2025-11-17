from pico2d import *
from player import *
from enemy import *
from shop import Shop
from ui import PlayerUI, EnemyUI
import game_world
import framework
import time
from background_manager import BackgroundManager

player = None

# 충돌 쿨다운(초)
COLLISION_COOLDOWN = 0.5
LAST_COLLISION_TIME = 0.0

def init():
    global player, background_manager
    # 객체들 생성
    player = Player()
    background_manager = BackgroundManager()
    enemy1 = Gorgon(600, 200, 0)
    enemy2 = Gorgon(700, 300, 1)
    enemy3 = Gorgon(300, 100, 2)
    shop = Shop()
    player_ui = PlayerUI(player)

    # 게임 월드에 객체들 추가
    game_world.add_object(player, 1)
    game_world.add_object(background_manager.background, 0)
    game_world.add_object(enemy1, 1)
    game_world.add_object(enemy2, 1)
    game_world.add_object(enemy3, 1)
    game_world.add_object(shop, 0)
    game_world.add_object(player_ui, 2)

    # 충돌 쌍 등록
    game_world.add_collision_pair( 'player:enemy', player, None)
    game_world.add_collision_pair( 'player:item', player, None)
    game_world.add_collision_pair( 'player:enemy', None, enemy1)
    game_world.add_collision_pair( 'player:enemy', None, enemy2)
    game_world.add_collision_pair( 'player:enemy', None, enemy3)
    game_world.add_collision_pair('attack:enemy', None, enemy1)
    game_world.add_collision_pair('attack:enemy', None, enemy2)
    game_world.add_collision_pair('attack:enemy', None, enemy3)
    game_world.add_collision_pair('player:shop', player, shop)


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        else:
            player.handle_event(event)

def update():
    global LAST_COLLISION_TIME
    game_world.update()
    if background_manager:
        old_background = background_manager.background
        background_manager.check_stage_transition(player)
        # 배경이 변경되었다면 game_world에서도 교체
        if old_background != background_manager.background:
            game_world.remove_object(old_background)
            game_world.add_object(background_manager.background, 0)

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