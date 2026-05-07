import asyncio
from aiogram import Bot, Dispatcher, types
from src.adapters.base import BaseAdapter, BridgeMessage
from config.settings import settings

class TelegramAdapter(BaseAdapter):
    def __init__(self):
        self.bot = Bot(token=settings.TG_TOKEN)
        self.dp = Dispatcher()
    async def start(self, engine):
        self.engine = engine
        @self.dp.message()
        async def h(m: types.Message):
            if m.chat.id != int(settings.TG_CHAT_ID): return
            await self.engine.handle_message(BridgeMessage(str(m.from_user.id), m.text or m.caption or 'Media', 'Telegram'))
        asyncio.create_task(self.dp.start_polling(self.bot))
    async def send_message(self, m): await self.bot.send_message(settings.TG_CHAT_ID, f'[{m.platform} {m.sender_id}]: {m.text}')
    async def send_file(self, m): pass