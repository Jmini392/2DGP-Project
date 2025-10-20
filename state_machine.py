from event_to_string import event_to_string

class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.next_state = None
        self.rules = rules
        self.cur_state.enter(('START', None))

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_event(self, state_event):
        # state_event가 어떤 이벤트 인지 체크할 수 있어야함
        for check_event in self.rules[self.cur_state].keys():
            if check_event(state_event):
                # 다음 상태 저장
                self.next_state = self.rules[self.cur_state][check_event]
                # 현재 상태 종료
                self.cur_state.exit(state_event)
                # 다음 상태 진입
                self.next_state.enter(state_event)
                # 상태 변환 디버그 프린트
                print(f'{self.cur_state.__class__.__name__} - {event_to_string(state_event)} -> {self.next_state.__class__.__name__}')
                # 현재 상태에서 다음상태로 전환
                self.cur_state = self.next_state
                return
        # 처리되지 않은 이벤트 디버그 프린트
        print(f'처리되지 않은 이벤트{event_to_string(state_event)}가 있습니다. ')