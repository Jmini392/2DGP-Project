from pico2d import *
import framework
import random
import share

#merchant frame
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

merchant_list = ['sprite/merchant1.png', 'sprite/merchant2.png']
merchant_index = 0

class Shop:
    def __init__(self):
        self.frame = 0
        self.merchant_index = random.randint(0, 1)
        global merchant_index
        merchant_index = self.merchant_index
        self.merchant_image = load_image(merchant_list[self.merchant_index])
        self.shop_image = load_image('sprite/shop.png')
        self.shop_x, self.shop_y = 1000, 340

    def draw(self):
        self.merchant_image.clip_draw(int(self.frame) * 64, 0, 64, 64, self.shop_x - 130, self.shop_y - 40, 100, 100)
        self.shop_image.draw(self.shop_x, self.shop_y, 166, 184)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 8

    def get_bb(self):
        return self.shop_x - 170, self.shop_y - 110, self.shop_x + 100, self.shop_y + 100

    def handle_collision(self, group, other):
        pass

class Stand:
    def __init__(self):
        self.merchant_img = load_image(f'sprite/merchant{merchant_index + 1}.png')
        self.image = load_image('sprite/stand.png')
        self.arrow = load_image('sprite/arrow.png')
        self.frame = 0
        self.font = load_font('Galmuri14.TTF', 50)
        self.x = 220

    def draw(self):
        self.merchant_img.clip_draw(int(self.frame) * 64, 0, 64, 64, 990, 400, 600, 600)
        self.image.draw(720, 350, 1494, 1656)
        self.font.draw(220, 250, '100G', (255, 255, 0))
        self.font.draw(440, 250, '150G', (255, 255, 0))
        self.font.draw(660, 250, '200G', (255, 255, 0))
        self.font.draw(180, 150, f'{share.player.inventory.get('speed')}개', (0, 0, 0))
        self.font.draw(400, 150, f'{share.player.inventory.get('strong')}개', (0, 0, 0))
        self.font.draw(620, 150, f'{share.player.inventory.get('health')}개', (0, 0, 0))
        self.font.draw(800, 150, f'소지금: {share.player.inventory.get('money')}G', (255, 255, 0))
        self.arrow.rotate_draw(math.radians(270), self.x, 500, 70, 70)

    def arrow_move(self, x = 0):
        if x == 220:
            if self.x < 660:
                self.x += 220
        elif x == -220:
            if self.x > 220:
                self.x -= 220

    def buy_item(self):
        # 상점 아이템 클릭 처리 로직 구현
        if self.x == 220:
            # 속도 아이템 구매
            if share.player.inventory['money'] >= 100:
                share.player.inventory['money'] -= 100
                share.player.inventory['speed'] += 1
        elif self.x == 440:
            # 공격력 아이템 구매
            if share.player.inventory['money'] >= 150:
                share.player.inventory['money'] -= 150
                share.player.inventory['strong'] += 1
        elif self.x == 660:
            # 체력 아이템 구매
            if share.player.inventory['money'] >= 200:
                share.player.inventory['money'] -= 200
                share.player.inventory['health'] += 1

    def update(self):
        self.frame = (self.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * framework.frame_time) % 8
