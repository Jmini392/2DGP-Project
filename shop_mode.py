from pico2d import *
import framework
import game_world
from shop import Stand

stand = None
player = None
font = None

def init():
    global stand, font
    stand = Stand()
    game_world.add_object(stand, 2)
    font = load_font('Galmuri14.TTF', 50)

def get_player_data(Player):
    global player
    player = Player

def shop_item_click(x, y):
    # 상점 아이템 클릭 처리 로직 구현
    if 133 <= x <= 254 and 350 <= y <= 480:
        # 속도 아이템 구매
        if player.inventory['money'] >= 100:
            player.inventory['money'] -= 100
            player.inventory['speed'] += 1
    elif 357 <= x <= 484 and 350 <= y <= 480:
        # 공격력 아이템 구매
        if player.inventory['money'] >= 150:
            player.inventory['money'] -= 150
            player.inventory['strong'] += 1
    elif 582 <= x <= 715 and 350 <= y <= 480:
        # 체력 아이템 구매
        if player.inventory['money'] >= 200:
            player.inventory['money'] -= 200
            player.inventory['health'] += 1

def finish():
    game_world.remove_object(stand)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_v:
            framework.pop_mode()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == 1:
            shop_item_click(event.x, event.y)
            print(f"Mouse Clicked at ({event.x}, {event.y})")

def draw():
    clear_canvas()
    game_world.render()
    font.draw(220, 250, '100G', (255, 255, 0))
    font.draw(440, 250, '150G', (255, 255, 0))
    font.draw(660, 250, '200G', (255, 255, 0))
    font.draw(180, 150, f'{player.inventory.get('speed')}개', (0, 0, 0))
    font.draw(400, 150, f'{player.inventory.get('strong')}개', (0, 0, 0))
    font.draw(620, 150, f'{player.inventory.get('health')}개', (0, 0, 0))
    font.draw(800, 150, f'소지금: {player.inventory.get('money')}G', (255, 255, 0))
    update_canvas()

def update():
    game_world.update()

def pause():
    pass

def resume():
    pass