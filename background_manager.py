from background import Background
import game_world
import framework

class BackgroundManager:
    def __init__(self):
        self.current_stage = 0
        self.max_stage = 10
        self.background = Background(0)

    def draw(self):
        self.background.draw()

    def update(self):
        pass

    def check_stage_transition(self, player):
        if player.x >= 1280 - 64:
            # 마지막 스테이지인 경우 더 이상 진행하지 않음
            if self.current_stage == self.max_stage:
                return
            # 몬스터가 남아있는 경우 진행하지 않음
            if game_world.is_empty():
                return
            # 다음 스테이지로 진행
            self.current_stage += 1
            # 배경이 바뀌는 경우에만 새 배경 생성
            if self.current_stage == 3:
                self.background = Background(1)
            elif self.current_stage == 7:
                self.background = Background(2)
            elif self.current_stage == 10:
                self.background = Background(3)
            # 플레이어 위치 초기화
            player.x = 0