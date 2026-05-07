from fastapi import FastAPI, Header
from src.core.engine import engine
from src.adapters.base import BridgeMessage
from config.settings import settings

app = FastAPI()
@app.post('/send')
async def send(text: str, x_token: str = Header(None)):
    if x_token != settings.API_TOKEN: return {'error': 'unauthorized'}
    await engine.handle_message(BridgeMessage('API', text, 'HTTP-API'))
    return {'status': 'sent'}