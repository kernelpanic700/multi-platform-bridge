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
        # Create 3 adapters
        tg = self.create_mock_adapter('telegram')
        mx = self.create_mock_adapter('matrix')
        tm = self.create_mock_adapter('teams')
        
        self.engine.register_adapter(tg)
        self.engine.register_adapter(mx)
        self.engine.register_adapter(tm)
        
        # Message received from Telegram
        msg = BridgeMessage(sender_id='123', text='Hello', platform='telegram', message_id='msg1')
        
        await self.engine.handle_message(msg)
        
        # Telegram should not receive its own message
        tg.send_message.assert_not_called()
        # Others should receive it
        mx.send_message.assert_called_once_with(msg)
        tm.send_message.assert_called_once_with(msg)

    async def test_engine_file_routing(self):
        tg = self.create_mock_adapter('telegram')
        mx = self.create_mock_adapter('matrix')
        self.engine.register_adapter(tg)
        self.engine.register_adapter(mx)
        
        # Message with file from Telegram
        msg = BridgeMessage(sender_id='123', text='File', platform='telegram', message_id='msg2', file_path='/tmp/test.txt')
        
        await self.engine.handle_message(msg)
        
        mx.send_file.assert_called_once_with(msg)
        mx.send_message.assert_not_called()

    async def test_engine_duplicate_handling(self):
        # Mock state_manager to always return True (duplicate)
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
        
        # Matrix will throw an error
        mx.send_message.side_effect = Exception('Network error')
        
        self.engine.register_adapter(tg)
        self.engine.register_adapter(mx)
        self.engine.register_adapter(tm)
        
        msg = BridgeMessage(sender_id='123', text='Hello', platform='telegram', message_id='msg4')
        
        # Call should not fail
        await self.engine.handle_message(msg)
        
        # Teams should still receive the message despite the Matrix error
        tm.send_message.assert_called_once_with(msg)

if __name__ == '__main__':
    unittest.main()