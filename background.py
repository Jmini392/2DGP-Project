from pico2d import load_image

background = ['sprite/Fieldground.png', 'sprite/Forestground.png', 'sprite/Battleground.png']

class Background:
    def __init__(self,stage = 0, x = 640, y = 360):
        self.x, self.y = x, y
        self.stage = stage
        self.image = load_image(background[self.stage])

    def draw(self):
        self.image.clip_draw(0, 0, 1920, 1080, self.x, self.y, 1280, 720)

    def update(self):
        pass