"import httpx
import logging
import time
from src.adapters.base import BaseAdapter, BridgeMessage
from config.settings import settings

class TeamsAdapter(BaseAdapter):
    def __init__(self):
        self.platform = 'teams'
        self.token = None
        self.token_expires_at = 0
        self.http_client = None

    async def _ensure_client(self):
        if self.http_client is None:
            self.http_client = httpx.AsyncClient()
        return self.http_client

    async def _get_token(self):
        if self.token and time.time() < (self.token_expires_at - 60):
            return self.token
        
        url = f"https://login.microsoftonline.com/{settings.TEAMS_TENANT_ID}/oauth2/v2.0/token"
        data = {
            "client_id": settings.TEAMS_CLIENT_ID,
            "client_secret": settings.TEAMS_CLIENT_SECRET,
            "grant_type": "client_credentials",
            "scope": "https://graph.microsoft.com/.default"
        }
        
        client = await self._ensure_client()
        resp = await client.post(url, data=data)
        resp.raise_for_status()
        res_data = resp.json()
        self.token = res_data.get('access_token')
        self.token_expires_at = time.time() + res_data.get('expires_in', 3600)
        return self.token

    async def start(self, engine):
        self.engine = engine
        await self._ensure_client()
        await self._get_token()

    async def send_message(self, m: BridgeMessage):
        token = await self._get_token()
        if not token:
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        client = await self._ensure_client()
        body = {"body": {"content": f"[{m.platform} {m.sender_id}]: {m.text}"}}
        
        for channel_id in settings.TEAMS_CHANNELS:
            try:
                await client.post(
                    f"https://graph.microsoft.com/v1.0/teams/{channel_id}/channels/general/messages",
                    headers=headers,
                    json=body
                )
            except Exception as e:
                logging.error(f"Teams send_message error to {channel_id}: {e}")

    async def send_file(self, m: BridgeMessage):
        logging.info(f"Teams send_file requested for {m.file_name}. (Feature partially implemented)")
        await self.send_message(BridgeMessage(
            sender_id=m.sender_id,
            text=f"{m.text}\n📎 File: {m.file_name}",
            platform=m.platform,
            message_id=m.message_id
        ))

    async def handle_webhook_event(self, data):
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

    async def close(self):
        if self.http_client:
            await self.http_client.aclose()
            self.http_client = None"