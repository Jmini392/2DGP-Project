from background import Background
import game_world
import framework

class BackgroundManager:
    def __init__(self):
        self.current_stage = 0
        self.count = 0  # 스테이지 카운트
        self.max_stage = 2  # 최대 스테이지 번호
        self.stage_repeat_count = { # 각 스테이지별 반복 횟수 설정
            0: 3,  # 1번 배경: 3번 반복
            1: 3,  # 2번 배경: 3번 반복
            2: 4  # 3번 배경: 4번 반복
        }
        self.background = Background(self.current_stage)

    def draw(self):
        self.background.draw()

    def check_stage_transition(self, player):
        # 다음 스테이지로
        if player.x >= 1280 - 64:
            self.count += 1
            # 마지막 스테이지의 마지막 반복일 경우 더 이상 진행하지 않음
            if self.current_stage == self.max_stage and self.count >= self.stage_repeat_count[self.current_stage]:
                return
            # 현재 스테이지의 반복 횟수만큼 반복
            if self.count >= self.stage_repeat_count[self.current_stage]:
                self.count = 0
                if self.current_stage < self.max_stage:
                    self.current_stage += 1
                    print(f"Stage {self.current_stage}로 이동")
            player.x = 0  # 플레이어를 왼쪽 끝으로 이동
            self.background = Background(self.current_stage)