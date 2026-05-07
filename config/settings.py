from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    TG_TOKEN: str = Field(..., env='TG_TOKEN')
    TG_CHAT_ID: str = Field(..., env='TG_CHAT_ID')
    MATRIX_HOMESERVER: str = Field('https://matrix.org', env='MATRIX_HOMESERVER')
    MATRIX_USER: str = Field(..., env='MATRIX_USER')
    MATRIX_PASSWORD: str = Field(..., env='MATRIX_PASSWORD')
    MATRIX_ROOM_ID: str = Field(..., env='MATRIX_ROOM_ID')
    TEAMS_TENANT_ID: str = Field(..., env='TEAMS_TENANT_ID')
    TEAMS_CLIENT_ID: str = Field(..., env='TEAMS_CLIENT_ID')
    TEAMS_CLIENT_SECRET: str = Field(..., env='TEAMS_CLIENT_SECRET')
    TEAMS_CHANNEL_ID: str = Field(..., env='TEAMS_CHANNEL_ID')
    API_PORT: int = 8000
    API_TOKEN: str = Field('secret-bridge-token', env='API_TOKEN')

    class Config:
        env_file = '.env'

settings = Settings()