from pico2d import *
import game_world

class Item:
    def __init__(self):
        pass
        self.x, self.y = 400, 300
        # 아이템 이미지 로드
        self.image = load_image('sprite/potion.png')

    def draw(self):
        pass
        # 아이템 그리기
        self.image.clip_draw(0, 0, 1800, 1800,self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        pass

    def handle_collision(self, group, other):
        if group == 'player:item':
            game_world.remove_object(self)