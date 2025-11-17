from player import Player
from enemy import Gorgon, Wizard
from shop import Shop
from ui import PlayerUI
import game_world


class StageManager:
    def __init__(self):
        self.current_stage = 0
        self.player = None
        self.player_ui = None
        self.enemies = []

    def init_player(self):
        if not self.player:
            self.player = Player()
            self.player_ui = PlayerUI(self.player)
            game_world.add_object(self.player, 1)
            game_world.add_object(self.player_ui, 2)
            game_world.add_collision_pair('player:enemy', self.player, None)
            game_world.add_collision_pair('player:item', self.player, None)

    def load_stage(self, stage_num):
        self.current_stage = stage_num

        # 일반 몬스터 스테이지
        if self.current_stage == 0 or self.current_stage == 1:
            self.load_stage_0()
            pass
        # 상점 스테이지
        elif self.current_stage == 2 or self.current_stage == 6 or self.current_stage == 9:
            self.load_stage_shop()
        # 에픽 몬스터 스테이지
        elif self.current_stage == 3 or self.current_stage == 4:
            self.load_stage_1()
            pass
        # 중간 보스 몬스터 스테이지
        elif self.current_stage == 5:
            self.load_stage_2()
            pass
        # 엘리트 몬스터 스테이지
        elif self.current_stage == 7 or self.current_stage == 8:
            self.load_stage_3()
        # 보스 몬스터 스테이지
        elif self.current_stage == 10:
            self.load_final_stage()

    def load_stage_0(self):
        enemy1 = Gorgon(600, 200, 0)
        enemy2 = Gorgon(900, 300, 0)
        self.enemies = [enemy1, enemy2]

        for enemy in self.enemies:
            game_world.add_object(enemy, 1)
            game_world.add_collision_pair('player:enemy', None, enemy)
            game_world.add_collision_pair('attack:enemy', None, enemy)

    def load_stage_1(self):
        enemy1 = Gorgon(500, 250, 1)
        enemy2 = Gorgon(700, 150, 1)
        self.enemies = [enemy1, enemy2]

        for enemy in self.enemies:
            game_world.add_object(enemy, 1)
            game_world.add_collision_pair('player:enemy', None, enemy)
            game_world.add_collision_pair('attack:enemy', None, enemy)

    def load_stage_2(self):
        enemy1 = Gorgon(500, 250, 2)
        enemy2 = Gorgon(700, 150, 2)
        self.enemies = [enemy1, enemy2]

        for enemy in self.enemies:
            game_world.add_object(enemy, 1)
            game_world.add_collision_pair('player:enemy', None, enemy)
            game_world.add_collision_pair('attack:enemy', None, enemy)

    def load_stage_3(self):
        enemy1 = Wizard(600, 200, 0)
        enemy2 = Wizard(900, 300, 0)
        self.enemies = [enemy1, enemy2]

        for enemy in self.enemies:
            game_world.add_object(enemy, 1)
            game_world.add_collision_pair('player:enemy', None, enemy)
            game_world.add_collision_pair('attack:enemy', None, enemy)

    def load_stage_shop(self):
        shop = Shop()
        game_world.add_object(shop, 0)
        game_world.add_collision_pair('player:shop', None, shop)

    def load_final_stage(self):
        pass