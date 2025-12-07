from pico2d import *
import game_world
import framework
import time
from player import Player
from background_manager import BackgroundManager
from stage_manager import StageManager
import title_mode
import shop_mode
import share

# 충돌 쿨다운(초)
COLLISION_COOLDOWN = 0.2
LAST_COLLISION_TIME = 0.0
y = 720

def init():
    if share.player is None:
        share.player = Player()
        game_world.add_object(share.player, 1)
        game_world.add_collision_pair('player:enemy', share.player, None)
        game_world.add_collision_pair('player:item', share.player, None)
        game_world.add_collision_pair('player:shop', share.player, None)

    global background_manager, stage_manager, game_over, font, blink_timer, show_text, ending
    background_manager = BackgroundManager()
    game_world.add_object(background_manager, 0)
    stage_manager = StageManager()
    stage_manager.load_stage(0)
    game_over = load_image('sprite/game_over.png')
    ending = load_image('sprite/the_end.png')
    font = load_font('Galmuri14.TTF', 50)
    blink_timer = 0.0
    show_text = True
    share.bgm = load_music('sound/1.mp3')
    share.bgm.repeat_play()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_v:
            if share.player.shopping:
                game_world.remove_object(share.player.ui)
                framework.push_mode(shop_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if share.player.over or share.player.win:
                share.player = None
                game_world.clear()
                framework.change_mode(title_mode)
                share.bgm = load_music('sound/title.mp3')
                share.bgm.repeat_play()
        else:
            share.player.handle_event(event)

def update():
    global LAST_COLLISION_TIME
    game_world.update()
    stage_manager.update()

    old_stage = background_manager.current_stage
    old_background = background_manager.background
    # 플레이어 위치에 따라 스테이지 전환 체크
    background_manager.check_stage_transition(share.player)
    # 스테이지가 변경되었다면
    if old_stage != background_manager.current_stage:
        # 배경이 실제로 바뀐 경우에만 처리
        if old_background != background_manager.background:
            # game_world.remove_object(old_background)
            game_world.add_object(background_manager.background, 0)
        # 새로운 스테이지 객체 로드
        stage_manager.load_stage(background_manager.current_stage)

    if share.player.over or share.player.win:
        global y, blink_timer, show_text
        if y > 450:
            y -= 100 * framework.frame_time
        blink_timer += framework.frame_time
        if blink_timer >= 0.5:
            blink_timer = 0.0
            show_text = not show_text

    now = time.time()
    if now - LAST_COLLISION_TIME >= COLLISION_COOLDOWN:
        game_world.handle_collisions()
        LAST_COLLISION_TIME = now

def draw():
    clear_canvas()
    game_world.render()
    global y
    if share.player.over:
        game_over.draw(640, y, 1280, 720)
        if y <= 450 and show_text:
            font.draw(250, 220, '스페이스바를 눌러 타이틀로 돌아가기', (255, 255, 0))
    elif share.player.win:
        ending.draw(640, y, 1280, 720)
        if y <= 450 and show_text:
            font.draw(250, 220, '스페이스바를 눌러 타이틀로 돌아가기', (255, 255, 0))
    update_canvas()

def finish():
    pass

def pause():
    pass

def resume():
    if background_manager.current_stage < 3:
        share.bgm = load_music('sound/1.mp3')
        share.bgm.repeat_play()
    elif background_manager.current_stage < 7:
        share.bgm = load_music('sound/2.mp3')
        share.bgm.repeat_play()
    elif background_manager.current_stage < 10:
        share.bgm = load_music('sound/3.mp3')
        share.bgm.repeat_play()