class StateManager:
    def __init__(self):
        self.seen_messages = set()
    def is_duplicate(self, message_id: str) -> bool:
        if message_id in self.seen_messages: return True
        self.seen_messages.add(message_id)
        return False

state_manager = StateManager()