from fastapi import FastAPI, Request, Header, HTTPException
import uuid
from src.core.engine import engine
from src.adapters.base import BridgeMessage
from config.settings import settings

app = FastAPI()

def get_adapter_by_platform(platform: str):
    for adapter in engine.adapters:
        if getattr(adapter, 'platform', '').lower() == platform.lower():
            return adapter
    return None

@app.post("/webhooks/teams")
async def teams_webhook(request: Request):
    try:
        data = await request.json()
        adapter = get_adapter_by_platform('teams')
        if not adapter:
            raise HTTPException(status_code=500, detail="Teams adapter not found")
        
        await adapter.handle_webhook_event(data)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/send")
async def external_send(request: Request, x_token: str = Header(None)):
    if x_token != settings.API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API token")
    
    try:
        data = await request.json()
        # Создаем сообщение от имени внешней системы (API)
        message = BridgeMessage(
            sender_id=data.get('sender_id', 'ExternalAPI'),
            text=data.get('text', ''),
            platform='api',
            message_id=f"api_{uuid.uuid4()}",
            file_path=data.get('file_path'),
            file_name=data.get('file_name')
        )
        await engine.handle_message(message)
        return {"status": "sent", "message_id": message.message_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))