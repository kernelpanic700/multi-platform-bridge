import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.core.engine import BridgeEngine
from src.adapters.base import BridgeMessage, BaseAdapter

class TestBridgeEngine(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = BridgeEngine()

    def create_mock_adapter(self, platform):
        adapter = MagicMock(spec=BaseAdapter)
        adapter.platform = platform
        adapter.send_message = AsyncMock()
        adapter.send_file = AsyncMock()
        return adapter

    async def test_engine_routing(self):
        # Создаем 3 адаптера
        tg = self.create_mock_adapter('telegram')
        mx = self.create_mock_adapter('matrix')
        tm = self.create_mock_adapter('teams')
        
        self.engine.register_adapter(tg)
        self.engine.register_adapter(mx)
        self.engine.register_adapter(tm)
        
        # Сообщение пришло из Telegram
        msg = BridgeMessage(sender_id='123', text='Hello', platform='telegram', message_id='msg1')
        
        await self.engine.handle_message(msg)
        
        # Telegram не должен получить свое же сообщение
        tg.send_message.assert_not_called()
        # Остальные должны получить
        mx.send_message.assert_called_once_with(msg)
        tm.send_message.assert_called_once_with(msg)

    async def test_engine_file_routing(self):
        tg = self.create_mock_adapter('telegram')
        mx = self.create_mock_adapter('matrix')
        self.engine.register_adapter(tg)
        self.engine.register_adapter(mx)
        
        # Сообщение с файлом из Telegram
        msg = BridgeMessage(sender_id='123', text='File', platform='telegram', message_id='msg2', file_path='/tmp/test.txt')
        
        await self.engine.handle_message(msg)
        
        mx.send_file.assert_called_once_with(msg)
        mx.send_message.assert_not_called()

    async def test_engine_duplicate_handling(self):
        # Мокаем state_manager, чтобы он всегда возвращал True (дубликат)
        with patch('src.core.engine.state_manager') as mock_sm:
            mock_sm.is_duplicate.return_value = True
            
            tg = self.create_mock_adapter('telegram')
            mx = self.create_mock_adapter('matrix')
            self.engine.register_adapter(tg)
            self.engine.register_adapter(mx)
            
            msg = BridgeMessage(sender_id='123', text='Hello', platform='telegram', message_id='msg3')
            await self.engine.handle_message(msg)
            
            mx.send_message.assert_not_called()

    async def test_engine_error_isolation(self):
        tg = self.create_mock_adapter('telegram')
        mx = self.create_mock_adapter('matrix')
        tm = self.create_mock_adapter('teams')
        
        # Matrix будет кидать ошибку
        mx.send_message.side_effect = Exception('Network error')
        
        self.engine.register_adapter(tg)
        self.engine.register_adapter(mx)
        self.engine.register_adapter(tm)
        
        msg = BridgeMessage(sender_id='123', text='Hello', platform='telegram', message_id='msg4')
        
        # Вызов не должен упасть
        await self.engine.handle_message(msg)
        
        # Teams всё равно должен получить сообщение, несмотря на ошибку Matrix
        tm.send_message.assert_called_once_with(msg)

if __name__ == '__main__':
    unittest.main()