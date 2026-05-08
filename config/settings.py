import yaml
import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    # Секреты из .env
    TG_TOKEN: str = Field(..., env='TG_TOKEN')
    MATRIX_HOMESERVER: str = Field('https://matrix.org', env='MATRIX_HOMESERVER')
    MATRIX_USER: str = Field(..., env='MATRIX_USER')
    MATRIX_PASSWORD: str = Field(..., env='MATRIX_PASSWORD')
    TEAMS_TENANT_ID: str = Field(..., env='TEAMS_TENANT_ID')
    TEAMS_CLIENT_ID: str = Field(..., env='TEAMS_CLIENT_ID')
    TEAMS_CLIENT_SECRET: str = Field(..., env='TEAMS_CLIENT_SECRET')
    API_PORT: int = 8000
    API_TOKEN: str = Field('secret-bridge-token', env='API_TOKEN')

    # Списки каналов из YAML
    TG_CHATS: List[str] = []
    MATRIX_ROOMS: List[str] = []
    TEAMS_CHANNELS: List[str] = []

    class Config:
        env_file = '.env'

    def load_bridge_config(self):
        config_path = 'config/bridge_config.yaml'
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data:
                    self.TG_CHATS = data.get('telegram', {}).get('chats', [])
                    self.MATRIX_ROOMS = data.get('matrix', {}).get('rooms', [])
                    self.TEAMS_CHANNELS = data.get('teams', {}).get('channels', [])

settings = Settings()
settings.load_bridge_config()