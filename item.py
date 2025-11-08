from pico2d import *
import game_world

potion_image = ['sprite/potion1.png', 'sprite/potion2.png', 'sprite/potion3.png']

class Item:
    image = None
    def __init__(self, x = 400, y = 200, type = 0):
        pass
        self.x, self.y = x, y
        self.type = type
        self.list = {
            0 : 'speed',
            1 : 'strong',
            2 : 'health'
        }
        if Item.image is None:
            self.image = load_image(potion_image[self.type])

    def draw(self):
        pass
        # 아이템 그리기
        self.image.clip_draw(0, 0, 568, 568, self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def update(self):
        pass

    def handle_collision(self, group, other):
        if group == 'player:item':
            game_world.remove_object(self)