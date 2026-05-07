import httpx
from src.adapters.base import BaseAdapter, BridgeMessage
from config.settings import settings

class TeamsAdapter(BaseAdapter):
    async def start(self, engine): self.engine = engine
    async def send_message(self, m): pass
    async def send_file(self, m): pass
    async def handle_webhook_event(self, data):
        await self.engine.handle_message(BridgeMessage(data.get('from', {}).get('id'), data.get('body', {}).get('content'), 'Teams'))