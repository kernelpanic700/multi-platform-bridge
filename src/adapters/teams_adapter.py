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
        # Token will be obtained on the first message send

    async def send_message(self, m: BridgeMessage):
        token = await self._get_token()
        if not token: return

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        for channel_id in settings.TEAMS_CHANNELS:
            try:
                async with httpx.AsyncClient() as client:
                    # Send message to a specific channel
                    await client.post(
                        f"https://graph.microsoft.com/v1.0/teams/{channel_id}/channels/general/messages",
                        headers=headers,
                        json={"body": {"content": f"[{m.platform} {m.sender_id}]: {m.text}"}}
                    )
            except Exception as e:
                logging.error(f"Teams send_message error to {channel_id}: {e}")

    async def send_file(self, m: BridgeMessage):
        # Implementation of file upload to MS Teams via Graph API
        # Requires uploading to Drive, obtaining a link, and sending a message with an attachment
        logging.info(f"Teams send_file requested for {m.file_name}. (Feature partially implemented)")
        # In this version, we send a text notification about the file
        await self.send_message(BridgeMessage(
            m.sender_id, 
            f"{m.text}\n📎 File: {m.file_name}", 
            m.platform, 
            m.message_id
        ))

    async def handle_webhook_event(self, data):
        # Processing data from Microsoft Teams webhook
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