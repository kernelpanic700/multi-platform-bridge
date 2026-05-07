import logging
from src.adapters.base import BaseAdapter, BridgeMessage
from src.core.state import state_manager

class BridgeEngine:
    def __init__(self): self.adapters = []
    def register_adapter(self, adapter): self.adapters.append(adapter)
    async def handle_message(self, message: BridgeMessage):
        msg_hash = f"{message.platform}:{message.sender_id}:{message.text}"
        if state_manager.is_duplicate(msg_hash): return
        for adapter in self.adapters:
            if adapter.__class__.__name__.lower().startswith(message.platform.lower()): continue
            try:
                if message.file_path: await adapter.send_file(message)
                else: await adapter.send_message(message)
            except Exception as e: print(f'Error: {e}')

engine = BridgeEngine()