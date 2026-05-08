from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class BridgeMessage:
    sender_id: str
    text: str
    platform: str
    message_id: str  # Unique message ID from the source platform
    file_path: Optional[str] = None
    file_name: Optional[str] = None

class BaseAdapter(ABC):
    @abstractmethod
    async def start(self, engine): pass
    @abstractmethod
    async def send_message(self, message: BridgeMessage): pass
    @abstractmethod
    async def send_file(self, message: BridgeMessage): pass