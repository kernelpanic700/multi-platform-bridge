import os
import uuid
from pathlib import Path
import logging
import aiofiles

class MediaUtils:
    TEMP_DIR = Path('/tmp/bridge_bot')

    @classmethod
    def ensure_temp_dir(cls):
        try:
            cls.TEMP_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.error(f'Failed to create temp dir: {e}')

    @classmethod
    def get_temp_path(cls, filename: str) -> str:
        cls.ensure_temp_dir()
        # Создаем уникальное имя, чтобы файлы разных пользователей не перемешались
        unique_name = f'{uuid.uuid4()}_{filename}'
        return str(cls.TEMP_DIR / unique_name)

    @classmethod
    async def save_content(cls, content: bytes, filename: str) -> str:
        path = cls.get_temp_path(filename)
        try:
            async with aiofiles.open(path, mode='wb') as f:
                await f.write(content)
            return path
        except Exception as e:
            logging.error(f'Error saving file {filename}: {e}')
            return None

    @classmethod
    def delete_file(cls, path: str):
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                logging.error(f'Error deleting file {path}: {e}')