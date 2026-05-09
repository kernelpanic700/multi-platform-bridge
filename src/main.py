"""Main entry point for the Bridge Bot application."""
import asyncio
import uvicorn
from src.core.engine import engine
from src.adapters.telegram_adapter import TelegramAdapter
from src.adapters.matrix_adapter import MatrixAdapter
from src.adapters.teams_adapter import TeamsAdapter
from src.api.server import app
from config.settings import settings


async def main():
    """Initialize all adapters and start the API server."""
    tg = TelegramAdapter()
    mx = MatrixAdapter()
    tm = TeamsAdapter()

    for adapter in [tg, mx, tm]:
        engine.register_adapter(adapter)

    await tg.start(engine)
    await mx.start(engine)
    await tm.start(engine)

    config = uvicorn.Config(app, host='0.0.0.0', port=settings.API_PORT)
    await uvicorn.Server(config).serve()


if __name__ == '__main__':
    asyncio.run(main())