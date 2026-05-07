"from collections import deque

class StateManager:
    def __init__(self, max_size=10000):
        self.max_size = max_size
        self.seen_messages = set()
        self.order = deque()

    def is_duplicate(self, message_id: str) -> bool:
        if message_id in self.seen_messages:
            return True
        
        self.seen_messages.add(message_id)
        self.order.append(message_id)
        
        if len(self.order) > self.max_size:
            oldest = self.order.popleft()
            self.seen_messages.discard(oldest)
            
        return False

state_manager = StateManager()"