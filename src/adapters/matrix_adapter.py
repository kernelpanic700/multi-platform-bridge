import asyncio
from nio import AsyncClient
from src.adapters.base import BaseAdapter, BridgeMessage
from config.settings import settings

class MatrixAdapter(BaseAdapter):
    def __init__(self): self.client = AsyncClient(settings.MATRIX_HOMESERVER, settings.MATRIX_USER)
    async def start(self, engine):
        self.engine = engine
        await self.client.login(settings.MATRIX_PASSWORD)
        asyncio.create_task(self._sync())
    async def _sync(self):
        while True:
            events = await self.client.sync(timeout=30000)
            for e in events['room_events']:
                if e.room_id == settings.MATRIX_ROOM_ID and e.type == 'm.room.message':
                    await self.engine.handle_message(BridgeMessage(e.sender, e.body, 'Matrix'))
            await asyncio.sleep(1)
    async def send_message(self, m): await self.client.room_send(settings.MATRIX_ROOM_ID, 'm.room.message', {'msgtype': 'text', 'body': f'[{m.platform} {m.sender_id}]: {m.text}'})
    async def send_file(self, m): pass