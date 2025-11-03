from pico2d import load_image

background = ['sprite/Fieldground.png', 'sprite/Forestground.png', 'sprite/Battleground.png']

class Background:
    def __init__(self):
        self.stage = 0
        self.image = load_image(background[self.stage])

    def draw(self):
        self.image.clip_draw(0, 0, 1920, 1080, 400,300,800,600)

    def update(self):
        pass