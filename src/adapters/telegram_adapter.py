import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from src.adapters.base import BaseAdapter, BridgeMessage
from config.settings import settings
from src.utils.media import MediaUtils

class TelegramAdapter(BaseAdapter):
    def __init__(self):
        self.platform = 'telegram'
        self.bot = Bot(token=settings.TG_TOKEN)
        self.dp = Dispatcher()

    async def start(self, engine):
        self.engine = engine
        
        @self.dp.message()
        async def h(m: types.Message):
            # Check if the chat is in the allowed list
            if str(m.chat.id) not in settings.TG_CHATS:
                return

            text = m.text or m.caption or 'Media'
            msg_id = str(m.message_id)
            file_path, file_name = None, None

            # Handle media files
            if m.document:
                file = await self.bot.get_file(m.document.file_id)
                file_name = m.document.file_name
                file_path = await self.bot.download_file(file.file_path)
                # Rewrite path via MediaUtils for consistency
                content = await asyncio.to_thread(lambda: open(file_path, 'rb').read())
                file_path = await MediaUtils.save_content(content, file_name)
                MediaUtils.delete_file(file_path) # Delete temporary aiogram file
            
            await self.engine.handle_message(BridgeMessage(
                sender_id=str(m.from_user.id),
                text=text,
                platform=self.platform,
                message_id=f"tg_{msg_id}",
                file_path=file_path,
                file_name=file_name
            ))

        asyncio.create_task(self.dp.start_polling(self.bot))

    async def send_message(self, m: BridgeMessage):
        for chat_id in settings.TG_CHATS:
            try:
                await self.bot.send_message(chat_id, f'[{m.platform} {m.sender_id}]: {m.text}')
            except Exception as e:
                logging.error(f"TG send_message error to {chat_id}: {e}")

    async def send_file(self, m: BridgeMessage):
        for chat_id in settings.TG_CHATS:
            try:
                with open(m.file_path, 'rb') as f:
                    await self.bot.send_document(chat_id, f, caption=f'[{m.platform} {m.sender_id}]: {m.text}')
            except Exception as e:
                logging.error(f"TG send_file error to {chat_id}: {e}")