"import logging
from src.adapters.base import BaseAdapter, BridgeMessage
from src.core.state import state_manager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BridgeEngine:
    def __init__(self):
        self.adapters = []

    def register_adapter(self, adapter): 
        self.adapters.append(adapter)

    async def handle_message(self, message: BridgeMessage):
        # Используем уникальный ID сообщения для проверки на дубликаты
        if state_manager.is_duplicate(message.message_id):
            return

        logging.info(f\"Routing message from {message.platform} ({message.sender_id})\")

        for adapter in self.adapters:
            # Пропускаем адаптер, который прислал сообщение
            if getattr(adapter, 'platform', '').lower() == message.platform.lower():
                continue
            
            try:
                if message.file_path:
                    await adapter.send_file(message)
                else:
                    await adapter.send_message(message)
            except Exception as e:
                logging.error(f\"Error sending message to {adapter.__class__.__name__}: {e}\")

engine = BridgeEngine()"