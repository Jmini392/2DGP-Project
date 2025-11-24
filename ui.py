from pico2d import *
from player import *
from enemy import *
from item import *

def draw_thick_rectangle(x1, y1, x2, y2, color=(255, 255, 0), thickness=3):
    # 네 꼭짓점 정의
    p1 = (x1, y1)  # 좌하단
    p2 = (x2, y1)  # 우하단
    p3 = (x2, y2)  # 우상단
    p4 = (x1, y2)  # 좌상단
    # 네 변을 각각 두껍게 그리기
    edges = [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]
    for (x1, y1), (x2, y2) in edges:
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            continue
        # 수직 방향 단위 벡터
        nx = -dy / length
        ny = dx / length
        # 두께만큼 오프셋하여 여러 선 그리기
        half = (thickness - 1) / 2.0
        for i in range(thickness):
            offset = i - half
            ox = nx * offset
            oy = ny * offset
            draw_line(x1 + ox, y1 + oy, x2 + ox, y2 + oy, *color)

class PlayerUI:
    def __init__(self, player):
        self.x , self.y = 100, 660
        self.player = player
        self.player_image = load_image('sprite/player_portrait.png')
        self.font = load_font('ENCR10B.TTF', 20)
        self.item_image = [load_image('sprite/potion1.png'), load_image('sprite/potion2.png'), load_image('sprite/potion3.png')]

    def draw(self):
        # 플레이어 초상화 및 체력바 그리기
        self.player_image.clip_draw(0, 0, 40, 40, self.x - 50, self.y + 10, 80, 80)
        draw_thick_rectangle(self.x - 90, self.y - 30, self.x - 10, self.y + 50, (255, 255, 0), 3)
        draw_rectangle(self.x, self.y, self.x + self.player.health * 4, self.y + 30, 255, 255, 0, 0, True)
        self.font.draw(self.x + 10, self.y + 10, f'{self.player.health}/{self.player.max_health}', (0, 0, 0))
        draw_thick_rectangle(self.x, self.y, self.x + self.player.max_health * 4, self.y + 30, (255, 255, 0), 5)
        # 인벤토리 그리기
        self.item_image[0].clip_draw(0, 0, 568, 568, 125, 625, 50, 50)
        self.font.draw(100, 640, f'{self.player.inventory.get('speed')}', (0, 0, 0))
        self.item_image[1].clip_draw(0, 0, 568, 568, 175, 625, 50, 50)
        self.font.draw(150, 640, f'{self.player.inventory.get('strong')}', (0, 0, 0))
        self.item_image[2].clip_draw(0, 0, 568, 568, 225, 625, 50, 50)
        self.font.draw(200, 640, f'{self.player.inventory.get('health')}', (0, 0, 0))
        if self.player.item is 'speed':
            draw_thick_rectangle(100, 600, 150, 650, (0, 0, 0))
        elif self.player.item is 'strong':
            draw_thick_rectangle(150, 600, 200, 650, (0, 0, 0))
        elif self.player.item is 'health':
            draw_thick_rectangle(200, 600, 250, 650, (0, 0, 0))

    def update(self):
        pass

class EnemyUI:
    def __init__(self, enemy, type = 0, num = 0):
        self.enemy = enemy
        self.type = type
        self.num = num
        self.x , self.y = 1250, 680
        if self.type == 0:
            self.image = load_image('sprite/Gorgon_portrait1.png')
        elif self.type == 1:
            self.image = load_image('sprite/Gorgon_portrait2.png')
        elif self.type == 2:
            self.image = load_image('sprite/Gorgon_portrait3.png')
        elif self.type == 3:
            self.image = load_image('sprite/Wizard_portrait.png')

    def draw(self):
        # 플레이어 초상화 및 체력바 그리기
        self.image.clip_draw(0, 0, 32, 32, self.x, self.y - (self.num * 50), 40, 40)
        draw_thick_rectangle(self.x - 20, self.y + 20 - (self.num * 50), self.x + 20, self.y - 20- (self.num * 50), (255, 255, 0), 3)
        draw_rectangle(self.x - 30, self.y - (self.num * 50), self.x - self.enemy.health * 2 - 30, self.y - 20 - (self.num * 50), 255, 255, 0, 0, True)

    def update(self):
        pass