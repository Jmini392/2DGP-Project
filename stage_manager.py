from player import Player
from enemy import Gorgon, Wizard
from shop import Shop
from ui import PlayerUI, EnemyUI
import game_world


class StageManager:
    def __init__(self):
        self.current_stage = 0
        self.player = None
        self.player_ui = None
        self.enemies = []
        self.enemy_uis = {}  # 적과 UI를 매핑하는 딕셔너리

    def init_player(self):
        if not self.player:
            self.player = Player()
            self.player_ui = PlayerUI(self.player)
            game_world.add_object(self.player, 1)
            game_world.add_object(self.player_ui, 2)
            game_world.add_collision_pair('player:enemy', self.player, None)
            game_world.add_collision_pair('player:item', self.player, None)
            game_world.add_collision_pair('player:shop', self.player, None)

    def update(self):
        """죽은 적의 UI를 제거"""
        dead_enemies = []
        for enemy in self.enemies[:]:  # 리스트 복사본으로 반복
            if not game_world.find_object(enemy):
                dead_enemies.append(enemy)
                if enemy in self.enemy_uis:
                    ui = self.enemy_uis[enemy]
                    game_world.remove_object(ui)
                    del self.enemy_uis[enemy]

        for enemy in dead_enemies:
            if enemy in self.enemies:
                self.enemies.remove(enemy)

    def load_stage(self, stage_num):
        self.current_stage = stage_num
        self.enemy_uis.clear()  # 새 스테이지 로드 시 UI 매핑 초기화

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
        enemy1 = Wizard(600, 200, 0)
        enemy1ui = EnemyUI(enemy1, 3, 0)
        game_world.add_object(enemy1ui, 2)
        self.enemy_uis[enemy1] = enemy1ui

        enemy2 = Gorgon(900, 300, 0)
        enemy2ui = EnemyUI(enemy2, 0, 1)
        game_world.add_object(enemy2ui, 2)
        self.enemy_uis[enemy2] = enemy2ui

        self.enemies = [enemy1, enemy2]

        for enemy in self.enemies:
            game_world.add_object(enemy, 1)
            game_world.add_collision_pair('player:enemy', None, enemy)
            game_world.add_collision_pair('attack:enemy', None, enemy)

    def load_stage_1(self):
        enemy1 = Gorgon(500, 250, 1)
        enemy1ui = EnemyUI(enemy1, 1, 0)
        game_world.add_object(enemy1ui, 2)
        self.enemy_uis[enemy1] = enemy1ui

        enemy2 = Gorgon(700, 150, 1)
        enemy2ui = EnemyUI(enemy2, 1, 1)
        game_world.add_object(enemy2ui, 2)
        self.enemy_uis[enemy2] = enemy2ui

        self.enemies = [enemy1, enemy2]

        for enemy in self.enemies:
            game_world.add_object(enemy, 1)
            game_world.add_collision_pair('player:enemy', None, enemy)
            game_world.add_collision_pair('attack:enemy', None, enemy)

    def load_stage_2(self):
        enemy1 = Gorgon(500, 250, 2)
        enemy1ui = EnemyUI(enemy1, 2, 0)
        game_world.add_object(enemy1ui, 2)
        self.enemy_uis[enemy1] = enemy1ui

        enemy2 = Gorgon(700, 150, 2)
        enemy2ui = EnemyUI(enemy2, 2, 1)
        game_world.add_object(enemy2ui, 2)
        self.enemy_uis[enemy2] = enemy2ui

        self.enemies = [enemy1, enemy2]

        for enemy in self.enemies:
            game_world.add_object(enemy, 1)
            game_world.add_collision_pair('player:enemy', None, enemy)
            game_world.add_collision_pair('attack:enemy', None, enemy)

    def load_stage_3(self):
        enemy1 = Wizard(600, 200, 0)
        enemy1ui = EnemyUI(enemy1, 3, 0)
        game_world.add_object(enemy1ui, 2)
        self.enemy_uis[enemy1] = enemy1ui

        enemy2 = Wizard(900, 300, 0)
        enemy2ui = EnemyUI(enemy2, 3, 1)
        game_world.add_object(enemy2ui, 2)
        self.enemy_uis[enemy2] = enemy2ui

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