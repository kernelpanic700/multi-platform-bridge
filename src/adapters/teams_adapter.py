import httpx
import logging
from src.adapters.base import BaseAdapter, BridgeMessage
from config.settings import settings

class TeamsAdapter(BaseAdapter):
    def __init__(self):
        self.platform = 'teams'
        self.token = None

    async def _get_token(self):
        if self.token:
            return self.token
        
        url = f"https://login.microsoftonline.com/{settings.TEAMS_TENANT_ID}/oauth2/v2.0/token"
        data = {
            "client_id": settings.TEAMS_CLIENT_ID,
            "client_secret": settings.TEAMS_CLIENT_SECRET,
            "grant_type": "client_credentials",
            "scope": "https://graph.microsoft.com/.default"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, data=data)
                resp.raise_for_status()
                self.token = resp.json().get('access_token')
                return self.token
            except Exception as e:
                logging.error(f"Teams OAuth2 error: {e}")
                return None

    async def start(self, engine):
        self.engine = engine
        # Токен будет получен при первой отправке сообщения

    async def send_message(self, m: BridgeMessage):
        token = await self._get_token()
        if not token: return

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        for channel_id in settings.TEAMS_CHANNELS:
            try:
                async with httpx.AsyncClient() as client:
                    # Отправка сообщения в конкретный канал
                    await client.post(
                        f"https://graph.microsoft.com/v1.0/teams/{channel_id}/channels/general/messages",
                        headers=headers,
                        json={"body": {"content": f"[{m.platform} {m.sender_id}]: {m.text}"}}
                    )
            except Exception as e:
                logging.error(f"Teams send_message error to {channel_id}: {e}")

    async def send_file(self, m: BridgeMessage):
        # Реализация загрузки файла в MS Teams через Graph API
        # Требует загрузки в Drive, получения ссылки и отправки сообщения с вложением
        logging.info(f"Teams send_file requested for {m.file_name}. (Feature partially implemented)")
        # В данной версии отправляем текстовое уведомление о файле
        await self.send_message(BridgeMessage(
            m.sender_id, 
            f"{m.text}\n📎 File: {m.file_name}", 
            m.platform, 
            m.message_id
        ))

    async def handle_webhook_event(self, data):
        # Обработка данных из вебхука Microsoft Teams
        try:
            await self.engine.handle_message(BridgeMessage(
                sender_id=data.get('from', {}).get('id', 'TeamsUser'),
                text=data.get('body', {}).get('content', ''),
                platform=self.platform,
                message_id=data.get('id', 'unknown'),
                file_path=None,
                file_name=None
            ))
        except Exception as e:
            logging.error(f"Error handling Teams webhook: {e}")