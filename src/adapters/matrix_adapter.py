import asyncio
import logging
import httpx
from nio import AsyncClient, RoomMessageText, RoomMessageFile
from src.adapters.base import BaseAdapter, BridgeMessage
from config.settings import settings
from src.utils.media import MediaUtils

class MatrixAdapter(BaseAdapter):
    def __init__(self):
        self.platform = 'matrix'
        self.client = AsyncClient(settings.MATRIX_HOMESERVER, settings.MATRIX_USER)

    async def start(self, engine):
        self.engine = engine
        await self.client.login(settings.MATRIX_PASSWORD)
        asyncio.create_task(self._sync())

    async def _sync(self):
        while True:
            try:
                response = await self.client.sync(timeout=30000)
                for event in response.room_events:
                    if event.room_id in settings.MATRIX_ROOMS:
                        if isinstance(event, (RoomMessageText, RoomMessageFile)):
                            await self._process_event(event)
            except Exception as e:
                logging.error(f"Matrix sync error: {e}")
            await asyncio.sleep(1)

    async def _process_event(self, e):
        msg_id = e.event_id
        text = getattr(e, 'body', '')
        file_path, file_name = None, None

        if isinstance(e, RoomMessageFile):
            url = e.url
            file_name = e.filename or 'file'
            async with httpx.AsyncClient() as client:
                try:
                    resp = await client.get(url)
                    if resp.status_code == 200:
                        file_path = await MediaUtils.save_content(resp.content, file_name)
                except Exception as ex:
                    logging.error(f"Matrix file download error: {ex}")

        await self.engine.handle_message(BridgeMessage(
            sender_id=e.sender,
            text=text,
            platform=self.platform,
            message_id=f"mx_{msg_id}",
            file_path=file_path,
            file_name=file_name
        ))

    async def send_message(self, m: BridgeMessage):
        for room_id in settings.MATRIX_ROOMS:
            try:
                await self.client.room_send(room_id, 'm.room.message', {
                    'msgtype': 'm.text', 
                    'body': f'[{m.platform} {m.sender_id}]: {m.text}'
                })
            except Exception as e:
                logging.error(f"Matrix send_message error to {room_id}: {e}")

    async def send_file(self, m: BridgeMessage):
        if not m.file_path:
            return

        for room_id in settings.MATRIX_ROOMS:
            try:
                with open(m.file_path, 'rb') as f:
                    response = await self.client.upload(f.read(), m.file_name or 'file')
                
                await self.client.room_send(room_id, 'm.room.message', {
                    'msgtype': 'm.file',
                    'body': f'[{m.platform} {m.sender_id}]: {m.text}',
                    'url': response.content_uri,
                    'filename': m.file_name or 'file'
                })
            except Exception as e:
                logging.error(f"Matrix send_file error to {room_id}: {e}")